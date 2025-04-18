from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

# class User(models.Model):
#     username = models.CharField(max_length=150, unique=True)
#     email = models.EmailField(unique=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     password = models.CharField(max_length=128)
#
#     def __str__(self):
#         return self.username


# class Event(models.Model):
#     title = models.CharField(max_length=128)
#     date = models.DateField()
#     description = models.TextField()
#     location = models.CharField(max_length=128)
#     organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
#     participant = models.ManyToManyField(User, related_name='participated_events', blank=True)
#
#     def __str__(self):
#         return self.title
