from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import AnatomySystem, AnatomyStructure, AnatomyProgress
from core.models import Activity, StudentProfile
import json


@login_required
def anatomy_explorer(request):
    """Main anatomy explorer view - updated function name"""
    systems = AnatomySystem.objects.all().order_by('name')
    
    # Get user progress
    user_progress = AnatomyProgress.objects.filter(user=request.user)
    total_structures = AnatomyStructure.objects.count()
    viewed_structures = user_progress.count()
    
    context = {
        'systems': systems,
        'total_structures': total_structures,
        'viewed_structures': viewed_structures,
        'progress_percentage': round((viewed_structures / total_structures * 100), 1) if total_structures > 0 else 0,
    }
    return render(request, 'anatomy/anatomy_explorer.html', context)


@login_required
def anatomy_home(request):
    """Redirect to anatomy explorer"""
    return anatomy_explorer(request)


@login_required
def system_detail(request, system_id):
    system = get_object_or_404(AnatomySystem, id=system_id)
    structures = system.structures.all()
    
    # Get user progress for this system
    user_progress = AnatomyProgress.objects.filter(
        user=request.user,
        structure__system=system
    ).values_list('structure_id', flat=True)
    
    context = {
        'system': system,
        'structures': structures,
        'user_progress': list(user_progress),
        'progress_count': len(user_progress),
        'total_count': structures.count(),
    }
    return render(request, 'anatomy/system_detail.html', context)


@login_required
def structure_detail(request, structure_id):
    structure = get_object_or_404(AnatomyStructure, id=structure_id)
    
    # Record or update progress
    progress, created = AnatomyProgress.objects.get_or_create(
        user=request.user,
        structure=structure,
        defaults={'xp_earned': structure.xp_reward}
    )
    
    if created:
        # First time viewing - award XP
        try:
            profile = request.user.studentprofile
        except StudentProfile.DoesNotExist:
            profile = StudentProfile.objects.create(user=request.user)
        
        profile.add_xp(structure.xp_reward)
        
        # Record activity
        Activity.objects.create(
            user=request.user,
            activity_type='anatomy_explored',
            title=f'Explored Anatomy: {structure.name}',
            description=f'Studied {structure.name} in {structure.system.name}',
            xp_earned=structure.xp_reward
        )
    
    context = {
        'structure': structure,
        'progress': progress,
        'is_first_view': created,
    }
    return render(request, 'anatomy/structure_detail.html', context)


@login_required
def update_time_spent(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        structure_id = data.get('structure_id')
        time_spent = data.get('time_spent', 0)
        
        try:
            progress = AnatomyProgress.objects.get(
                user=request.user,
                structure_id=structure_id
            )
            progress.time_spent += time_spent
            progress.save()
            
            return JsonResponse({'success': True})
        except AnatomyProgress.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Progress not found'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})
