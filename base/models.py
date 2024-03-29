from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    isDoctor = models.BooleanField(default=False)

    
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


    

    





 
