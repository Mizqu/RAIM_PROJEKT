from django.shortcuts import render
from django.http import HttpResponse
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
import logging
from .forms import CustomAuthenticationForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Specialization
import json
from .models import DoctorInfo
from .forms import DoctorCreationForm

def index(request):
    if request.method == 'POST':
        form = DoctorCreationForm(request.POST)
        if form.is_valid():
            specializations = form.cleaned_data['specializations']
            bio = form.cleaned_data['bio']
            doctor_info = DoctorInfo.objects.create(user_id=request.user.id, bio=bio)
            doctor_info.specializations.set(specializations)           
            doctor_info.save()
            return redirect('index')
    else:
        form = DoctorCreationForm()
    return render(request, 'base/index.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('index'))   
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect(reverse('login'))  
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def logout_view(request):
    if request.method == 'GET':
        logout(request)
        return HttpResponseRedirect('/')
    