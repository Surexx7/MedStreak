from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid


def generate_student_id():
    return str(uuid.uuid4())[:8].upper()

class StudentProfile(models.Model):
    YEAR_CHOICES = [
        ('1', 'First Year'),
        ('2', 'Second Year'),
        ('3', 'Third Year'),
        ('4', 'Fourth Year'),
        ('resident', 'Resident'),
        ('other', 'Other'),
    ]
    
    SPECIALIZATION_CHOICES = [
        ('general', 'General Medicine'),
        ('cardiology', 'Cardiology'),
        ('neurology', 'Neurology'),
        ('pediatrics', 'Pediatrics'),
        ('surgery', 'Surgery'),
        ('psychiatry', 'Psychiatry'),
        ('emergency', 'Emergency Medicine'),
        ('radiology', 'Radiology'),
        ('pathology', 'Pathology'),
        ('other', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id =  models.CharField(max_length=100, unique=True, default=generate_student_id)
    university = models.CharField(max_length=200, blank=True)
    year_of_study = models.CharField(max_length=10, choices=YEAR_CHOICES, default='1')
    specialization = models.CharField(max_length=20, choices=SPECIALIZATION_CHOICES, default='general')
    
    # Gamification fields
    total_xp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_activity = models.DateTimeField(default=timezone.now)
    
    # Academic progress
    cases_completed = models.IntegerField(default=0)
    quiz_accuracy = models.FloatField(default=0.0)
    total_study_time = models.IntegerField(default=0)  # in minutes
    timed_challenges_completed = models.IntegerField(default=0)
    
    # Profile settings
    is_profile_complete = models.BooleanField(default=False)
    email_notifications = models.BooleanField(default=True)
    public_profile = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - Level {self.level}"
    
    def add_xp(self, amount):
        """Add XP and handle level progression"""
        self.total_xp += amount
        # Level up logic: every 1000 XP = 1 level
        new_level = (self.total_xp // 1000) + 1
        if new_level > self.level:
            self.level = new_level
            # Create level up achievement
            Achievement.objects.get_or_create(
                user=self.user,
                achievement_type='level_up',
                defaults={
                    'title': f'Level {new_level} Reached!',
                    'description': f'Congratulations on reaching level {new_level}!',
                    'xp_reward': 50
                }
            )
        self.save()
    
    def update_streak(self):
        """Update daily streak"""
        today = timezone.now().date()
        last_activity_date = self.last_activity.date()
        
        if last_activity_date == today:
            return  # Already active today
        elif last_activity_date == today - timezone.timedelta(days=1):
            self.current_streak += 1
            if self.current_streak > self.longest_streak:
                self.longest_streak = self.current_streak
        else:
            self.current_streak = 1
        
        self.last_activity = timezone.now()
        self.save()
        
        # Check for streak achievements
        if self.current_streak >= 7:
            Achievement.objects.get_or_create(
                user=self.user,
                achievement_type='streak_7',
                defaults={
                    'title': 'Week Warrior',
                    'description': '7-day learning streak!',
                    'xp_reward': 100
                }
            )
        if self.current_streak >= 30:
            Achievement.objects.get_or_create(
                user=self.user,
                achievement_type='streak_30',
                defaults={
                    'title': 'Month Master',
                    'description': '30-day learning streak!',
                    'xp_reward': 500
                }
            )
    
    def get_rank(self):
        """Get user's rank based on XP"""
        return StudentProfile.objects.filter(total_xp__gt=self.total_xp).count() + 1
    
    def get_level_progress(self):
        """Get progress to next level as percentage"""
        current_level_xp = self.total_xp % 1000
        return (current_level_xp / 1000) * 100
    
    def get_xp_to_next_level(self):
        """Get XP needed for next level"""
        return 1000 - (self.total_xp % 1000)


class Achievement(models.Model):
    ACHIEVEMENT_TYPES = [
        ('case_master', 'Case Master'),
        ('quiz_expert', 'Quiz Expert'),
        ('streak_7', 'Week Warrior'),
        ('streak_30', 'Month Master'),
        ('anatomy_explorer', 'Anatomy Explorer'),
        ('ai_user', 'AI User'),
        ('level_up', 'Level Up'),
        ('first_case', 'First Case'),
        ('perfect_quiz', 'Perfect Quiz'),
        ('early_bird', 'Early Bird'),
        ('night_owl', 'Night Owl'),
        ('first_timed_challenge', 'First Timed Challenge'), 
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement_type = models.CharField(max_length=30, choices=ACHIEVEMENT_TYPES)
    title = models.CharField(max_length=100)
    description = models.TextField()
    xp_reward = models.IntegerField(default=0)
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'achievement_type']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"

class Activity(models.Model):
    ACTIVITY_TYPES = [
        ('case_completed', 'Case Completed'),
        ('quiz_taken', 'Quiz Taken'),
        ('anatomy_explored', 'Anatomy Explored'),
        ('ai_checker_used', 'AI Checker Used'),
        ('achievement_earned', 'Achievement Earned'),
        ('level_up', 'Level Up'),
        ('login', 'Login'),
        ('profile_updated', 'Profile Updated'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    xp_earned = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Activities'
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"

class StudySession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.IntegerField(default=0)
    activities_completed = models.IntegerField(default=0)
    xp_earned = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.username} - {self.start_time.date()}"

class TimedChallengeAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    time_taken = models.IntegerField()  # in seconds
    xp_earned = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.score}/{self.total_questions} in {self.time_taken}s"

# Signal handlers - KEEP ONLY ONE SET!
@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    if created:
        StudentProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_student_profile(sender, instance, **kwargs):
    if hasattr(instance, 'studentprofile'):
        instance.studentprofile.save()

# Signal to update timed challenge count
@receiver(post_save, sender=TimedChallengeAttempt)
def update_timed_challenge_count(sender, instance, created, **kwargs):
    if created:
        profile = instance.user.studentprofile
        profile.timed_challenges_completed += 1
        profile.save()
        
        # Create achievement for first timed challenge
        if profile.timed_challenges_completed == 1:
            Achievement.objects.get_or_create(
                user=instance.user,
                achievement_type='first_timed_challenge',
                defaults={
                    'title': 'Time Attacker',
                    'description': 'Completed your first timed challenge!',
                    'xp_reward': 50
                }
            )