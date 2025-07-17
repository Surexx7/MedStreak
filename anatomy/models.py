from django.db import models
from django.contrib.auth.models import User


class AnatomySystem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='heart')
    color = models.CharField(max_length=7, default='#3B82F6')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class AnatomyStructure(models.Model):
    system = models.ForeignKey(AnatomySystem, on_delete=models.CASCADE, related_name='structures')
    name = models.CharField(max_length=200)
    description = models.TextField()
    function = models.TextField()
    location = models.CharField(max_length=200)
    image_url = models.URLField(blank=True)
    model_3d_url = models.URLField(blank=True)
    xp_reward = models.IntegerField(default=10)

    def __str__(self):
        return f"{self.system.name} - {self.name}"


class AnatomyProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    structure = models.ForeignKey(AnatomyStructure, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)
    time_spent = models.IntegerField(default=0, help_text="Time spent in seconds")
    xp_earned = models.IntegerField(default=0)

    class Meta:
        unique_together = ['user', 'structure']

    def __str__(self):
        return f"{self.user.username} - {self.structure.name}"
