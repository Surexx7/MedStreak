from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='question_images/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_answers_count(self):
        return self.answers.count()
    
    def get_reactions_count(self):
        return self.reactions.count()

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Answer by {self.author.username} on {self.question.title}"

class QuestionReaction(models.Model):
    REACTION_CHOICES = [
        ('like', '👍'),
        ('love', '❤️'),
        ('helpful', '💡'),
        ('confused', '😕'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='reactions')
    reaction_type = models.CharField(max_length=10, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ('user', 'question')
    
    def __str__(self):
        return f"{self.user.username} - {self.get_reaction_type_display()}"

class AnswerReaction(models.Model):
    REACTION_CHOICES = [
        ('like', '👍'),
        ('helpful', '💡'),
        ('disagree', '👎'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='reactions')
    reaction_type = models.CharField(max_length=10, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ('user', 'answer')
    
    def __str__(self):
        return f"{self.user.username} - {self.get_reaction_type_display()}"

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('question_reaction', 'Question Reaction'),
        ('question_answer', 'Question Answer'),
        ('answer_reaction', 'Answer Reaction'),
    ]
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)
    reaction_type = models.CharField(max_length=10, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Notification for {self.recipient.username} from {self.sender.username}"
    
    def get_message(self):
        if self.notification_type == 'question_reaction':
            reaction_emoji = dict(QuestionReaction.REACTION_CHOICES).get(self.reaction_type, '👍')
            return f"{self.sender.get_full_name() or self.sender.username} reacted {reaction_emoji} to your question"
        elif self.notification_type == 'question_answer':
            return f"{self.sender.get_full_name() or self.sender.username} answered your question"
        elif self.notification_type == 'answer_reaction':
            reaction_emoji = dict(AnswerReaction.REACTION_CHOICES).get(self.reaction_type, '👍')
            return f"{self.sender.get_full_name() or self.sender.username} reacted {reaction_emoji} to your answer"
        return "New notification"
    
    def get_url(self):
        if self.question:
            return f"/ai-checker/question/{self.question.id}/"
        return "/ai-checker/"