from django.db import models
from django.contrib.auth.models import User


class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    difficulty = models.CharField(max_length=20, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ])
    time_limit = models.IntegerField(help_text="Time limit in minutes")
    xp_reward = models.IntegerField(default=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    explanation = models.TextField(blank=True)
    points = models.IntegerField(default=10)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.quiz.title} - Q{self.order}"


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=500)
    label = models.CharField(max_length=1)
    is_correct = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.choice_text[:50]


class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    max_score = models.IntegerField(default=0)
    time_taken = models.IntegerField(help_text="Time taken in seconds")
    completed_at = models.DateTimeField(auto_now_add=True)
    xp_earned = models.IntegerField(default=0)

    class Meta:
        ordering = ['-completed_at']

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} ({self.score}/{self.max_score})"

    @property
    def percentage(self):
        if self.max_score > 0:
            return round((self.score / self.max_score) * 100, 1)
        return 0


class QuizAnswer(models.Model):
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)
    time_taken = models.IntegerField(help_text="Time taken for this question in seconds")

    def __str__(self):
        return f"{self.attempt.user.username} - {self.question}"
