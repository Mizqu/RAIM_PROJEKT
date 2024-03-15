from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    isDoctor = models.BooleanField(default=False)

class DoctorInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specializations = models.JSONField(null = False, default=dict)
    bio = models.TextField(max_length = 350, null=True, default='')


class Specialization(models.Model):
    name = models.CharField(max_length = 30, null=False)




 
