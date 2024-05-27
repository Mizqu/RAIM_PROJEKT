from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    isDoctor = models.BooleanField(default=False)
    friends = models.ManyToManyField('self', symmetrical=True, default=None)

    
class Specialization(models.Model):
    name = models.CharField(max_length = 30, null=False)
    def __str__(self):
        return self.name

class DoctorInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specializations = models.ManyToManyField(Specialization)
    lorem = models.TextField(max_length=350, null=True, default='')
    bio = models.TextField(max_length=350, null=True, default='')
    approved = models.BooleanField(default=False)
    rate = models.FloatField(default = 0)

    def __str__(self):
        return self.user.username


class Message(models.Model):
    author = models.CharField(max_length=100)       # Autor wiadomości
    recipient = models.CharField(max_length=100)    # Odbiorca wiadomości
    content = models.TextField()    # Zawartość wiadomości
    timestamp = models.DateTimeField(default=timezone.now)      # Czas wysłania wiadomości
    file = models.FileField(upload_to='chat_files/', blank=True, null=True)     # Plik

    def __str__(self):
        return f'{self.author} -> {self.recipient}: {self.content or self.file.name}'

