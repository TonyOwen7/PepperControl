from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Map

@receiver(post_save, sender=User)
def create_default_map(sender, instance, created, **kwargs):
    if created and not Map.objects.filter(user=instance, is_default=True).exists():
        # Define the default matrix
        university_matrix = [
            [
                [0, 2, 2, 0, 1, 0],
                [0, 0, 0, 0, 1, 0],
                [0, 1, 0, 0, 1, 2],
                [0, 0, 0, 0, 2, 0],
                [2, 1, 0, 1, 1, 2]
            ]
        ]

        # Define the default rooms dictionary
        rooms = {
            "Accueil": [1, 0, 1],  # [matrix_index, row_index, col_index]
            "Bureau des enseignants": [1, 4, 4],
            "Classe 1": [1, 0, 2],
            "Classe 2": [1, 2, 5],
            "Classe 3": [1, 4, 0],
            "Toilette": [1, 2, 5],
            "Escalier": [1, 4, 0],
            "Bureau du directeur": [1, 4, 5]
        }

        # Create the default map and set it as the current map
        Map.objects.create(
            user=instance,
            name="University Matrix",
            matrices=university_matrix,  # Use the matrices field
            rows=5,  # Number of rows
            cols=6,  # Number of columns
            rooms=rooms,  # Use the rooms field
            is_default=True,
            is_current=True
        )