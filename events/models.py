from django.db import models

from users.models import User


class Event(models.Model):
    title = models.CharField(max_length=128)
    date = models.DateField()
    description = models.TextField()
    location = models.CharField(max_length=128)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    participant = models.ManyToManyField(User, related_name='participated_events', blank=True)

    def __str__(self):
        return self.title
