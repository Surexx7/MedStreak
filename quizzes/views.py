from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import Quiz, QuizAttempt, QuizAnswer, Question
from core.models import StudentProfile, Activity
import json
import random
from core.models import TimedChallengeAttempt

@login_required
def quiz_list(request):
    quizzes = Quiz.objects.all().order_by('-created_at')
    user_attempts = QuizAttempt.objects.filter(user=request.user)
    
    # Add attempt info to quizzes
    for quiz in quizzes:
        quiz.user_attempts = user_attempts.filter(quiz=quiz).count()
        best_attempt = user_attempts.filter(quiz=quiz).order_by('-score').first()
        quiz.best_score = best_attempt.percentage if best_attempt else 0
    
    context = {
        'quizzes': quizzes,
        'total_quizzes': quizzes.count(),
    }
    return render(request, 'quizzes/quiz_list.html', context)


@login_required
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    user_attempts = QuizAttempt.objects.filter(user=request.user, quiz=quiz)
    best_attempt = user_attempts.order_by('-score').first()
    
    context = {
        'quiz': quiz,
        'attempts_count': user_attempts.count(),
        'best_attempt': best_attempt,
        'questions_count': quiz.questions.count(),
    }
    return render(request, 'quizzes/quiz_detail.html', context)


@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.prefetch_related('choices').all()
    
    if request.method == 'POST':
        # Process quiz submission
        answers_data = json.loads(request.POST.get('answers', '{}'))
        time_taken = int(request.POST.get('time_taken', 0))
        
        # Create quiz attempt
        attempt = QuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            time_taken=time_taken,
            max_score=sum(q.points for q in questions)
        )
        
        score = 0
        for question in questions:
            question_id = str(question.id)
            if question_id in answers_data:
                selected_choice_id = answers_data[question_id]['choice_id']
                selected_choice = question.choices.get(id=selected_choice_id)
                
                is_correct = selected_choice.is_correct
                if is_correct:
                    score += question.points
                
                QuizAnswer.objects.create(
                    attempt=attempt,
                    question=question,
                    selected_choice=selected_choice,
                    is_correct=is_correct,
                    time_taken=answers_data[question_id].get('time_taken', 0)
                )
        
        # Update attempt with final score
        attempt.score = score
        attempt.xp_earned = int((score / attempt.max_score) * quiz.xp_reward) if attempt.max_score > 0 else 0
        attempt.save()
        
        # Update student profile
        try:
            profile = request.user.studentprofile
        except StudentProfile.DoesNotExist:
            profile = StudentProfile.objects.create(user=request.user)
        
        profile.add_xp(attempt.xp_earned)
        
        # Record activity
        Activity.objects.create(
            user=request.user,
            activity_type='quiz_taken',
            title=f'Completed Quiz: {quiz.title}',
            description=f'Scored {attempt.percentage}% on {quiz.title}',
            xp_earned=attempt.xp_earned
        )
        
        messages.success(request, f'Quiz completed! You scored {attempt.percentage}% and earned {attempt.xp_earned} XP!')
        return redirect('quizzes:quiz_result', attempt_id=attempt.id)
    
    context = {
        'quiz': quiz,
        'questions': questions,
    }
    return render(request, 'quizzes/take_quiz.html', context)


@login_required
def quiz_result(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)
    answers = attempt.answers.select_related('question', 'selected_choice').all()
    
    context = {
        'attempt': attempt,
        'answers': answers,
    }
    return render(request, 'quizzes/quiz_result.html', context)

@login_required
def timed_challenge(request):
    # Get 10 random questions from all quizzes
    questions = list(Question.objects.all())
    random.shuffle(questions)
    questions = questions[:10]
    
    # Prepare question data for JavaScript
    question_data = []
    for q in questions:
        choices = list(q.choices.all())  # Convert to list to preserve order
        # Find the correct choice index
        correct_index = next((i for i, c in enumerate(choices) if c.is_correct), None)
        
        question_data.append({
            'id': q.id,
            'question': q.question_text,
            'options': [c.choice_text for c in choices],
            'correct': correct_index,
            'explanation': q.explanation or "No explanation available",
        })
    
    context = {
        'questions': json.dumps(question_data)  # Pass as JSON
    }
    return render(request, 'quizzes/timed_challenge.html', context)

@csrf_exempt
@login_required
def submit_timed_results(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        score = data.get('score')
        total_questions = data.get('total_questions')
        time_taken = data.get('time_taken')
        
        # Calculate XP (10 XP per correct answer)
        xp_earned = score * 10
        
        # Update student profile
        try:
            profile = request.user.studentprofile
        except StudentProfile.DoesNotExist:
            profile = StudentProfile.objects.create(user=request.user)
        
        profile.add_xp(xp_earned)
        profile.save()
        
        # Record timed challenge attempt
        TimedChallengeAttempt.objects.create(
            user=request.user,
            score=score,
            total_questions=total_questions,
            time_taken=time_taken,
            xp_earned=xp_earned
        )
        
        # Record activity
        Activity.objects.create(
            user=request.user,
            activity_type='timed_challenge',
            title='Completed Timed Challenge',
            description=f'Scored {score}/{total_questions} in timed challenge',
            xp_earned=xp_earned
        )
        
        return JsonResponse({
            'success': True,
            'xp_earned': xp_earned
        })
    return JsonResponse({'success': False})