from django.contrib import admin
from .models import User, DoctorInfo, Specialization


# Register your models here.

admin.site.register(User)

admin.site.register(DoctorInfo)
admin.site.register(Specialization)