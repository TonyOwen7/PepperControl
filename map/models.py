from django.db import models
from django.contrib.auth.models import User

class Map(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='maps')
    name = models.CharField(max_length=255)
    matrices = models.JSONField(default=list)  # Stores a list of 2D matrices
    rows = models.IntegerField(default=4)  # Number of rows in each matrix
    cols = models.IntegerField(default=4)  # Number of columns in each matrix
    rooms = models.JSONField(default=list)  # Stores the dictionary of rooms and their coordinates
    is_default = models.BooleanField(default=False)
    is_current = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (User: {self.user.username})"