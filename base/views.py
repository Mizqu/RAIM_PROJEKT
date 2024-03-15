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
            user = request.user
            specializations = form.cleaned_data.get('specializations')
            doctor_info = DoctorInfo.objects.create(
                user=user,
                specializations=json.dumps(specializations)
            )
            doctor_info.save()
    else:
        form = DoctorInputForm()
        doctor_specializations = Specialization.objects.all()
    context = {
        'doctorSpecializations': doctor_specializations,
        'form' : form
    }
    
    return render(request, 'base/index.html', context)


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
    