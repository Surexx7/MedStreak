from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from django.utils import timezone
from django.contrib import messages
from django.db.models import Sum
from .models import Case, CaseStep, Choice, CaseAttempt
from core.models import StudentProfile, Activity, Achievement

@login_required
def case_list(request):
    """List all available cases"""
    cases = Case.objects.filter(is_active=True)
    user_attempts = CaseAttempt.objects.filter(user=request.user, completed=True)
    completed_case_ids = user_attempts.values_list('case_id', flat=True)
    
    context = {
        'cases': cases,
        'completed_case_ids': completed_case_ids,
    }
    return render(request, 'cases/case_list.html', context)

@login_required
def start_case(request, case_id):
    """Start a new case attempt"""
    case = get_object_or_404(Case, id=case_id, is_active=True)
    
    # Create new attempt
    attempt = CaseAttempt.objects.create(
        user=request.user,
        case=case,
        current_step=1  # Start at step 1
    )
    
    # Initialize student profile if needed
    StudentProfile.objects.get_or_create(user=request.user)
    
    return redirect('case_step', attempt_id=attempt.id)

@login_required
def case_step(request, attempt_id):
    """Show current step in case simulation"""
    attempt = get_object_or_404(CaseAttempt, id=attempt_id, user=request.user)
    
    if attempt.completed:
        return redirect('case_complete', attempt_id=attempt.id)
    
    # Get current step object
    try:
        current_step = CaseStep.objects.get(
            case=attempt.case, 
            step_number=attempt.current_step
        )
    except CaseStep.DoesNotExist:
        # Case completed but not marked
        attempt.completed = True
        attempt.completed_at = timezone.now()
        attempt.save()
        return redirect('case_complete', attempt_id=attempt.id)
    
    # Calculate progress
    total_steps = attempt.case.steps.count()
    progress = (attempt.current_step / total_steps) * 100
    
    context = {
        'attempt': attempt,
        'case': attempt.case,
        'current_step': current_step,  # ← Changed from 'step' to 'current_step'
        'choices': current_step.choices.all(),  # ← Keep this for backward compatibility
        'progress': progress,
        'step_number': attempt.current_step,
        'total_steps': total_steps,
    }
    return render(request, 'cases/case_step.html', context)

@login_required
def submit_choice(request, attempt_id):
    """Submit choice for current step and move to next"""
    attempt = get_object_or_404(CaseAttempt, id=attempt_id, user=request.user)
    
    if attempt.completed:
        return JsonResponse({'error': 'Case already completed'}, status=400)
    
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid method'}, status=405)
    
    # Changed from 'choice_id' to 'choice' to match form
    choice_id = request.POST.get('choice')
    if not choice_id:
        return JsonResponse({'error': 'Missing choice ID'}, status=400)
    
    # Get selected choice
    try:
        choice = Choice.objects.get(id=choice_id, step__step_number=attempt.current_step)
    except Choice.DoesNotExist:
        return JsonResponse({'error': 'Invalid choice'}, status=400)
    
    # Record choice
    choices_made = attempt.get_choices_made()
    choices_made.append({
        'step': attempt.current_step,
        'choice_id': choice.id,
        'xp_earned': choice.xp_reward
    })
    attempt.choices_made = json.dumps(choices_made)
    attempt.total_xp_earned += choice.xp_reward
    attempt.save()
    
    # Update user profile
    profile = StudentProfile.objects.get(user=request.user)
    profile.add_xp(choice.xp_reward)
    profile.save()
    
    # Move to next step or complete
    next_step_number = attempt.current_step + 1
    has_next_step = CaseStep.objects.filter(
        case=attempt.case,
        step_number=next_step_number
    ).exists()
    
    if has_next_step:
        attempt.current_step = next_step_number
        attempt.save()
        return redirect('case_step', attempt_id=attempt.id)
    else:
        # Complete the case
        attempt.completed = True
        attempt.completed_at = timezone.now()
        attempt.save()
        
        # Update profile
        profile.cases_completed += 1
        profile.save()
        
        # Create activity
        Activity.objects.create(
            user=request.user,
            activity_type='case_completed',
            title=f'Completed "{attempt.case.title}"',
            description=f'Successfully completed the case simulation',
            xp_earned=attempt.total_xp_earned
        )
        
        # Check for achievements
        if profile.cases_completed >= 20:
            Achievement.objects.get_or_create(
                user=request.user,
                achievement_type='case_master',
                defaults={
                    'title': 'Case Master',
                    'description': 'Complete 20 cases',
                    'xp_reward': 100
                }
            )
        
        return redirect('case_complete', attempt_id=attempt.id)
    
@login_required
def case_complete(request, attempt_id):
    """Case completion summary view"""
    attempt = get_object_or_404(CaseAttempt, id=attempt_id, user=request.user)
    
    if not attempt.completed:
        return redirect('case_step', attempt_id=attempt.id)
    
    # Calculate performance metrics
    case = attempt.case
    max_possible_xp = Choice.objects.filter(
        step__case=case,
        is_correct=True
    ).aggregate(total_xp=Sum('xp_reward'))['total_xp'] or 0
    
    performance_score = 0
    if max_possible_xp > 0:
        performance_score = min(100, int((attempt.total_xp_earned / max_possible_xp) * 100))
    
    context = {
        'attempt': attempt,
        'case': case,
        'performance_score': performance_score,
        'max_possible_xp': max_possible_xp,
    }
    return render(request, 'cases/case_complete.html', context)