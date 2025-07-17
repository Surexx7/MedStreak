from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import json

from .models import Question, Answer, QuestionReaction, AnswerReaction, Notification
from .forms import QuestionForm, AnswerForm

def create_notification(recipient, sender, notification_type, question=None, answer=None, reaction_type=None):
    """Helper function to create notifications"""
    if recipient != sender:  # Don't notify yourself
        Notification.objects.create(
            recipient=recipient,
            sender=sender,
            notification_type=notification_type,
            question=question,
            answer=answer,
            reaction_type=reaction_type
        )

@login_required
def question_feed(request):
    """Main Q&A feed page - similar to Facebook home"""
    questions = Question.objects.select_related('author').prefetch_related(
        'answers__author', 'reactions'
    ).all()
    
    # Pagination
    paginator = Paginator(questions, 10)  # Show 10 questions per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get user's reactions for each question and add to question objects
    if request.user.is_authenticated:
        user_reactions = QuestionReaction.objects.filter(
            user=request.user,
            question__in=page_obj
        ).select_related('question')
        
        # Create a dictionary for quick lookup
        reactions_dict = {reaction.question.id: reaction.reaction_type for reaction in user_reactions}
        
        # Add user reaction to each question object
        for question in page_obj:
            question.user_reaction = reactions_dict.get(question.id, None)
    
    context = {
        'page_obj': page_obj,
        'question_form': QuestionForm(),
    }
    return render(request, 'ai_checker/question_feed.html', context)

@login_required
def ask_question(request):
    """Handle question creation"""
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            messages.success(request, 'Your question has been posted successfully!')
            return redirect('ai_checker:question_feed')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = QuestionForm()
    
    return render(request, 'ai_checker/ask_question.html', {'form': form})

@login_required
def question_detail(request, question_id):
    """Detailed view of a question with all answers"""
    question = get_object_or_404(Question, id=question_id)
    answers = question.answers.select_related('author').prefetch_related('reactions')
    
    # Handle answer submission
    if request.method == 'POST':
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            answer = answer_form.save(commit=False)
            answer.question = question
            answer.author = request.user
            answer.save()
            
            # Create notification for question author
            create_notification(
                recipient=question.author,
                sender=request.user,
                notification_type='question_answer',
                question=question,
                answer=answer
            )
            
            messages.success(request, 'Your answer has been posted!')
            return redirect('ai_checker:question_detail', question_id=question.id)
    else:
        answer_form = AnswerForm()
    
    # Get user's reactions
    user_question_reaction = None
    if request.user.is_authenticated:
        try:
            user_question_reaction = QuestionReaction.objects.get(
                user=request.user, question=question
            ).reaction_type
        except QuestionReaction.DoesNotExist:
            pass
        
        # Add user reactions to answer objects
        user_answer_reactions = AnswerReaction.objects.filter(
            user=request.user, answer__in=answers
        ).select_related('answer')
        
        reactions_dict = {reaction.answer.id: reaction.reaction_type for reaction in user_answer_reactions}
        
        for answer in answers:
            answer.user_reaction = reactions_dict.get(answer.id, None)
    
    context = {
        'question': question,
        'answers': answers,
        'answer_form': answer_form,
        'user_question_reaction': user_question_reaction,
    }
    return render(request, 'ai_checker/question_detail.html', context)

@login_required
@require_POST
def react_to_question(request, question_id):
    """Handle question reactions via AJAX"""
    question = get_object_or_404(Question, id=question_id)
    data = json.loads(request.body)
    reaction_type = data.get('reaction_type')
    
    if reaction_type not in dict(QuestionReaction.REACTION_CHOICES):
        return JsonResponse({'error': 'Invalid reaction type'}, status=400)
    
    reaction, created = QuestionReaction.objects.get_or_create(
        user=request.user,
        question=question,
        defaults={'reaction_type': reaction_type}
    )
    
    if not created:
        if reaction.reaction_type == reaction_type:
            # Remove reaction if clicking the same reaction
            reaction.delete()
            return JsonResponse({
                'status': 'removed',
                'reactions_count': question.get_reactions_count()
            })
        else:
            # Update reaction type
            reaction.reaction_type = reaction_type
            reaction.save()
    
    # Create notification for question author
    if created or reaction.reaction_type != reaction_type:
        create_notification(
            recipient=question.author,
            sender=request.user,
            notification_type='question_reaction',
            question=question,
            reaction_type=reaction_type
        )
    
    return JsonResponse({
        'status': 'added' if created else 'updated',
        'reaction_type': reaction_type,
        'reactions_count': question.get_reactions_count()
    })

@login_required
@require_POST
def react_to_answer(request, answer_id):
    """Handle answer reactions via AJAX"""
    answer = get_object_or_404(Answer, id=answer_id)
    data = json.loads(request.body)
    reaction_type = data.get('reaction_type')
    
    if reaction_type not in dict(AnswerReaction.REACTION_CHOICES):
        return JsonResponse({'error': 'Invalid reaction type'}, status=400)
    
    reaction, created = AnswerReaction.objects.get_or_create(
        user=request.user,
        answer=answer,
        defaults={'reaction_type': reaction_type}
    )
    
    if not created:
        if reaction.reaction_type == reaction_type:
            reaction.delete()
            return JsonResponse({
                'status': 'removed',
                'reactions_count': answer.reactions.count()
            })
        else:
            reaction.reaction_type = reaction_type
            reaction.save()
    
    # Create notification for answer author
    if created or reaction.reaction_type != reaction_type:
        create_notification(
            recipient=answer.author,
            sender=request.user,
            notification_type='answer_reaction',
            question=answer.question,
            answer=answer,
            reaction_type=reaction_type
        )
    
    return JsonResponse({
        'status': 'added' if created else 'updated',
        'reaction_type': reaction_type,
        'reactions_count': answer.reactions.count()
    })

@login_required
def notifications(request):
    """Display user notifications"""
    notifications = Notification.objects.filter(recipient=request.user).select_related(
        'sender', 'question', 'answer'
    )
    
    # Pagination
    paginator = Paginator(notifications, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'ai_checker/notifications.html', context)

@login_required
def get_notification_count(request):
    """Get unread notification count via AJAX"""
    unread_count = Notification.objects.filter(recipient=request.user, is_read=False).count()
    return JsonResponse({'unread_count': unread_count})

@login_required
@require_POST
def mark_notification_read(request, notification_id):
    """Mark a notification as read"""
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.is_read = True
    notification.save()
    return JsonResponse({'status': 'success'})

@login_required
@require_POST
def mark_all_notifications_read(request):
    """Mark all notifications as read"""
    Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
    return JsonResponse({'status': 'success'})

@login_required
def load_more_questions(request):
    """AJAX endpoint for infinite scroll"""
    page = request.GET.get('page', 1)
    questions = Question.objects.select_related('author').prefetch_related(
        'answers__author', 'reactions'
    ).all()
    
    paginator = Paginator(questions, 10)
    page_obj = paginator.get_page(page)
    
    questions_data = []
    for question in page_obj:
        questions_data.append({
            'id': question.id,
            'title': question.title,
            'content': question.content,
            'author': question.author.username,
            'created_at': question.created_at.strftime('%B %d, %Y at %I:%M %p'),
            'answers_count': question.get_answers_count(),
            'reactions_count': question.get_reactions_count(),
            'image_url': question.image.url if question.image else None,
        })
    
    return JsonResponse({
        'questions': questions_data,
        'has_next': page_obj.has_next(),
        'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
    })

@login_required
def notifications_json(request):
    """Get notifications in JSON format for dropdown"""
    limit = int(request.GET.get('limit', 10))
    notifications = Notification.objects.filter(recipient=request.user).select_related(
        'sender', 'question', 'answer'
    )[:limit]
    
    notifications_data = []
    for notification in notifications:
        notifications_data.append({
            'id': notification.id,
            'message': notification.get_message(),
            'sender_name': notification.sender.get_full_name() or notification.sender.username,
            'time_ago': notification.created_at.strftime('%B %d, %Y at %I:%M %p'),
            'is_read': notification.is_read,
            'url': notification.get_url(),
            'question_title': notification.question.title if notification.question else None,
        })
    
    return JsonResponse({'notifications': notifications_data})