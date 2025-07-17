from django.db import models
from django.contrib.auth.models import User
import json

class Case(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    category = models.CharField(max_length=100)
    patient_info = models.TextField()
    total_xp = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title

class CaseStep(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='steps')
    step_number = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    patient_info = models.TextField(blank=True)
    
    class Meta:
        ordering = ['step_number']
    
    def __str__(self):
        return f"{self.case.title} - Step {self.step_number}"

class Choice(models.Model):
    step = models.ForeignKey(CaseStep, on_delete=models.CASCADE, related_name='choices')
    text = models.TextField()
    xp_reward = models.IntegerField(default=0)
    is_correct = models.BooleanField(default=False)
    consequence = models.TextField()
    
    def __str__(self):
        return f"{self.step.title} - {self.text[:50]}"

class CaseAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    current_step = models.IntegerField(default=0)
    total_xp_earned = models.IntegerField(default=0)
    choices_made = models.TextField(default='[]')  # JSON field
    completed = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def get_choices_made(self):
        return json.loads(self.choices_made)
    
    def add_choice(self, choice_id, xp_earned):
        choices = self.get_choices_made()
        choices.append({'choice_id': choice_id, 'xp_earned': xp_earned})
        self.choices_made = json.dumps(choices)
        self.total_xp_earned += xp_earned
        self.save()
    
    def __str__(self):
        return f"{self.user.username} - {self.case.title}"
