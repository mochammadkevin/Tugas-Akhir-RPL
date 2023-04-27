from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    deadline = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete']

class Quote(models.Model):
    desc = models.TextField()

    def __str__(self):
        return self.desc

class Gratitude(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    desc = models.TextField()
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.desc


class Habit(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    emoji = models.CharField(max_length=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    saturday = models.BooleanField(default=False)
    sunday = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_progress(self):
        days_completed = sum([self.monday, self.tuesday, self.wednesday, self.thursday, self.friday, self.saturday, self.sunday])
        return f"{days_completed/7 * 100:.2f}%"
