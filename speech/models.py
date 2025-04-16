from django.db import models
from django.contrib.auth.models import User

class Speech(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='speeches')
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_favorite = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title