from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from django.http import JsonResponse
from .models import StudentProfile, Achievement, Activity, StudySession
from .forms import StudentRegistrationForm, StudentProfileForm, UserUpdateForm
from cases.models import Case
from django.contrib.auth.models import User
import google.generativeai as genai
from django.conf import settings 
import json
import asyncio
import time
from concurrent.futures import TimeoutError


def home(request):
    """Landing page view"""
    context = {
        'total_cases': Case.objects.count(),
        'total_students': StudentProfile.objects.count(),
        'success_rate': 95,  # Mock data
    }
    return render(request, 'core/home.html', context)

def register(request):
    """Student registration view"""
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create welcome activity
            Activity.objects.create(
                user=user,
                activity_type='login',
                title='Welcome to MediScope!',
                description='Account created successfully. Start your medical learning journey!',
                xp_earned=50
            )
            # Add welcome XP
            try:
                profile = user.studentprofile
                profile.add_xp(50)
            except StudentProfile.DoesNotExist:
                # profile = StudentProfile.objects.create(user=user)
                profile.add_xp(50)
            
            # Authenticate and login
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            
            messages.success(request, 'Welcome to MediScope! Your account has been created successfully.')
            return redirect('profile_setup')
    else:
        form = StudentRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile_setup(request):
    """Profile setup view for new students"""
    try:
        profile = request.user.studentprofile
    except StudentProfile.DoesNotExist:
        profile = StudentProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        profile_form = StudentProfileForm(request.POST, instance=profile)
        user_form = UserUpdateForm(request.POST, instance=request.user)
        
        if profile_form.is_valid() and user_form.is_valid():
            user_form.save()
            profile_form.save()
            profile.is_profile_complete = True
            profile.save()
            
            # Create profile completion activity
            Activity.objects.create(
                user=request.user,
                activity_type='profile_updated',
                title='Profile Completed',
                description='Successfully completed your student profile',
                xp_earned=25
            )
            profile.add_xp(25)
            
            messages.success(request, 'Your profile has been set up successfully!')
            return redirect('dashboard')
    else:
        profile_form = StudentProfileForm(instance=profile)
        user_form = UserUpdateForm(instance=request.user)
    
    context = {
        'profile_form': profile_form,
        'user_form': user_form,
    }
    return render(request, 'core/profile_setup.html', context)

@login_required
def dashboard(request):
    """Dashboard view with user stats and activities"""
    try:
        profile = request.user.studentprofile
    except StudentProfile.DoesNotExist:
        profile = StudentProfile.objects.create(user=request.user)
    
    # Update streak and create login activity
    profile.update_streak()
    
    # Create daily login activity (only once per day)
    today = timezone.now().date()
    login_today = Activity.objects.filter(
        user=request.user,
        activity_type='login',
        created_at__date=today
    ).exists()
    
    if not login_today:
        Activity.objects.create(
            user=request.user,
            activity_type='login',
            title='Daily Login',
            description=f'Logged in on {today.strftime("%B %d, %Y")}',
            xp_earned=5
        )
        profile.add_xp(5)
    
    # Get recent activities
    recent_activities = Activity.objects.filter(user=request.user)[:5]
    
    # Get recent achievements
    recent_achievements = Achievement.objects.filter(user=request.user)[:3]
    
    # Get leaderboard (top 10 users by XP)
    leaderboard = StudentProfile.objects.select_related('user').order_by('-total_xp')[:10]
    
    # Calculate user rank
    user_rank = profile.get_rank()
    
    # Get study stats
    today_sessions = StudySession.objects.filter(
        user=request.user,
        start_time__date=today
    )
    today_study_time = sum(session.duration_minutes for session in today_sessions)
    
    context = {
        'profile': profile,
        'recent_activities': recent_activities,
        'recent_achievements': recent_achievements,
        'leaderboard': leaderboard,
        'user_rank': user_rank,
        'xp_to_next_level': profile.get_xp_to_next_level(),
        'level_progress': profile.get_level_progress(),
        'today_study_time': today_study_time,
    }
    return render(request, 'core/dashboard.html', context)

@login_required
def profile(request):
    """User profile view and edit"""
    try:
        profile = request.user.studentprofile
    except StudentProfile.DoesNotExist:
        profile = StudentProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        profile_form = StudentProfileForm(request.POST, instance=profile)
        user_form = UserUpdateForm(request.POST, instance=request.user)
        
        if profile_form.is_valid() and user_form.is_valid():
            user_form.save()
            profile_form.save()
            
            # Create profile update activity
            Activity.objects.create(
                user=request.user,
                activity_type='profile_updated',
                title='Profile Updated',
                description='Successfully updated your profile information',
                xp_earned=10
            )
            profile.add_xp(10)
            
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        profile_form = StudentProfileForm(instance=profile)
        user_form = UserUpdateForm(instance=request.user)
    
    # Get all achievements
    achievements = Achievement.objects.filter(user=request.user).order_by('-earned_at')
    
    # Get study statistics
    total_sessions = StudySession.objects.filter(user=request.user).count()
    total_study_time = sum(
        session.duration_minutes for session in StudySession.objects.filter(user=request.user)
    )
    
    context = {
        'profile': profile,
        'profile_form': profile_form,
        'user_form': user_form,
        'achievements': achievements,
        'total_sessions': total_sessions,
        'total_study_time': total_study_time,
    }
    return render(request, 'core/profile.html', context)

@login_required
def leaderboard(request):
    """Leaderboard view"""
    # Get all students ordered by XP
    students = StudentProfile.objects.select_related('user').order_by('-total_xp')
    
    # Get current user's rank
    try:
        user_rank = request.user.studentprofile.get_rank()
    except StudentProfile.DoesNotExist:
        profile = StudentProfile.objects.create(user=request.user)
        user_rank = profile.get_rank()
    
    context = {
        'students': students,
        'user_rank': user_rank,
    }
    return render(request, 'core/leaderboard.html', context)

@login_required
def start_study_session(request):
    """Start a new study session"""
    if request.method == 'POST':
        # End any existing active sessions
        active_sessions = StudySession.objects.filter(
            user=request.user,
            end_time__isnull=True
        )
        for session in active_sessions:
            session.end_time = timezone.now()
            session.duration_minutes = int((session.end_time - session.start_time).total_seconds() / 60)
            session.save()
        
        # Create new session
        session = StudySession.objects.create(user=request.user)
        
        return JsonResponse({
            'success': True,
            'session_id': session.id,
            'message': 'Study session started!'
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@login_required
def end_study_session(request):
    """End current study session"""
    if request.method == 'POST':
        try:
            session = StudySession.objects.get(
                user=request.user,
                end_time__isnull=True
            )
            session.end_time = timezone.now()
            session.duration_minutes = int((session.end_time - session.start_time).total_seconds() / 60)
            session.save()
            
            # Add study time to profile
            try:
                profile = request.user.studentprofile
            except StudentProfile.DoesNotExist:
                profile = StudentProfile.objects.create(user=request.user)
            
            profile.total_study_time += session.duration_minutes
            profile.save()
            
            # Award XP for study time (1 XP per 5 minutes)
            xp_earned = session.duration_minutes // 5
            if xp_earned > 0:
                profile.add_xp(xp_earned)
                Activity.objects.create(
                    user=request.user,
                    activity_type='case_completed',
                    title=f'Study Session Completed',
                    description=f'Studied for {session.duration_minutes} minutes',
                    xp_earned=xp_earned
                )
            
            return JsonResponse({
                'success': True,
                'duration': session.duration_minutes,
                'xp_earned': xp_earned,
                'message': f'Study session completed! {session.duration_minutes} minutes'
            })
        except StudySession.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'No active study session found'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@csrf_exempt
def chatbot(request):
    if request.method == 'POST':
        start_time = time.time()
        
        try:
            # Handle both form data and JSON
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                user_input = data.get('message', '')
            else:
                user_input = request.POST.get('message', '')
            
            if not user_input:
                return JsonResponse({'error': 'No message provided'}, status=400)
            
            # Configure Gemini
            api_key = getattr(settings, 'GEMINI_API_KEY', None)
            if not api_key:
                return JsonResponse({
                    'error': 'GEMINI_API_KEY not found in settings'
                }, status=500)
            
            genai.configure(api_key=api_key)
            
            # Use the fastest model for better response time
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Optimize the prompt to be more concise
            prompt = f"Medical assistant: Answer this medical education question in 2-3 sentences: {user_input}"
            
            # Configure generation settings for faster response
            generation_config = {
                "temperature": 0.3,  # Lower temperature for faster, more focused responses
                "max_output_tokens": 500,  # Limit response length
                "top_k": 20,
                "top_p": 0.8,
            }
            
            # Generate response with timeout handling
            try:
                response = model.generate_content(
                    prompt,
                    generation_config=generation_config,
                    safety_settings=[
                        {
                            "category": "HARM_CATEGORY_HARASSMENT",
                            "threshold": "BLOCK_ONLY_HIGH"
                        },
                        {
                            "category": "HARM_CATEGORY_HATE_SPEECH",
                            "threshold": "BLOCK_ONLY_HIGH"
                        },
                        {
                            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                            "threshold": "BLOCK_ONLY_HIGH"
                        },
                        {
                            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                            "threshold": "BLOCK_ONLY_HIGH"
                        }
                    ]
                )
                
                # Check if response was blocked
                if not response.text:
                    return JsonResponse({
                        'reply': 'I apologize, but I cannot provide a response to that question. Please try rephrasing your medical question.'
                    })
                
                reply = response.text.strip()
                
                # Log response time for debugging
                response_time = time.time() - start_time
                print(f"Response time: {response_time:.2f} seconds")
                
                return JsonResponse({
                    'reply': reply,
                    'response_time': f"{response_time:.2f}s"
                })
                
            except Exception as api_error:
                # Handle API-specific errors
                error_msg = str(api_error)
                if "quota" in error_msg.lower():
                    return JsonResponse({
                        'reply': 'Service temporarily unavailable due to high demand. Please try again in a moment.'
                    })
                elif "timeout" in error_msg.lower():
                    return JsonResponse({
                        'reply': 'Response took too long. Please try a shorter question.'
                    })
                else:
                    raise api_error
            
        except Exception as e:
            response_time = time.time() - start_time
            print(f"Error after {response_time:.2f} seconds: {str(e)}")
            
            return JsonResponse({
                'error': f"Medical assistant error: {str(e)}",
                'response_time': f"{response_time:.2f}s"
            }, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)