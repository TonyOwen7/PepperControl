from django.db import models
from django.contrib.auth.models import User

class Robot(models.Model):
    # Define choices for the language field
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('fr', 'French'),
    ]
    
    # Define choices for direction
    DIRECTION_CHOICES = [
        ('up', 'Up'),
        ('right', 'Right'),
        ('down', 'Down'),
        ('left', 'Left'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='robots')
    name = models.CharField(max_length=100)
    nao_ip = models.CharField(max_length=15)
    network_interface = models.CharField(max_length=50)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='en')
    
    # New position fields
    floor = models.IntegerField(default=0)
    row = models.IntegerField(default=0)
    column = models.IntegerField(default=0)
    
    # Direction field
    direction = models.CharField(max_length=5, choices=DIRECTION_CHOICES, default='up')
    
    # Is current robot
    is_current = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # If this robot is being set as current, unset any other current robots for this user
        if self.is_current:
            Robot.objects.filter(user=self.user, is_current=True).exclude(id=self.id).update(is_current=False)
        super().save(*args, **kwargs)