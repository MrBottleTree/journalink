from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_CHOICES = [
        ('student', 'Student'),
        ('professor', 'Professor'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    department = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    reward_points = models.IntegerField(default=0)

    def __str__(self):
        return self.username
