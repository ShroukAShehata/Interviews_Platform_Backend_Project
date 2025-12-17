
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    
    #choices format is tuple of tuples , the first element to be stored in DB , second is human readable to appear in forms.
    ROLE_CHOICES = (
        ('expert', 'Expert'),
        ('explorer', 'Explorer'),
        ('admin', 'Admin'),   
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='explorer')
    experience_level = models.CharField(max_length=50, blank=True)
    bio = models.TextField(blank=True)


    def __str__(self):
        return f"{self.username} ({self.role})"
