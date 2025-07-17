from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from django.http import JsonResponse
from .models import StudentProfile, Achievement, Activity, StudySession
from .forms import StudentRegistrationForm, StudentProfileForm, UserUpdateForm
from cases.models import Case
from django.contrib.auth.models import User

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
