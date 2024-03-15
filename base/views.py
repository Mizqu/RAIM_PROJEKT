from django.shortcuts import render
from django.http import HttpResponse
from .forms import DoctorInputForm, CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
import logging
from .forms import CustomAuthenticationForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Specialization
import json
from .models import DoctorInfo

def index(request):
    if request.method == 'POST':
        form = DoctorInputForm(request.POST)
        if form.is_valid():
            doctor_info = form.save(commit=False)  # Tworzy obiekt DoctorInfo na podstawie danych z formularza
            doctor_info.user = request.user  # Przypisanie obiektu użytkownika do pola user
            doctor_info.save()  # Zapisanie obiektu DoctorInfo w bazie danych
            return redirect('index')
    else:
        form = DoctorInputForm()
    
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
    