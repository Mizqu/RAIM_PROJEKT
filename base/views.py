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
from .customfunctions import split_name


def index(request):
    if request.method == 'POST':
        form = DoctorCreationForm(request.POST)
        if form.is_valid():
            specializations = form.cleaned_data['specializations']
            bio = form.cleaned_data['lorem']
            doctor_info = DoctorInfo.objects.create(user_id=request.user.id, bio=bio)
            doctor_info.specializations.set(specializations)           
            doctor_info.save()
            return redirect('index')
    else:
        form = DoctorCreationForm()
    context = {
        'form': form,
        'Specializations': Specialization.objects.all()
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
    
def show_profile(request):
    user = request.user
    if user.isDoctor:
        doctorctx = True
        doctor_info = DoctorInfo.objects.get(user=user)
    else:
        doctorctx = False
        doctor_info = None
    context = {
        'doctorCtx' : doctorctx,  
        'user': user,
        'doctorInfo': doctor_info
    }
    return render(request, 'base/profile.html' , context)
   
def doctorSearch(request): 
    if request.method == 'GET':
        full_name = request.GET.get('full_name')
        specialization = request.GET.get('specialization')
        first_name, last_name = split_name(full_name)
    ListOfDoctors = []
    for doctor_info in DoctorInfo.objects.filter(approved=True):
        if doctor_info.user.first_name == first_name and doctor_info.user.last_name == last_name:
            ListOfDoctors.append(doctor_info)
        elif (doctor_info.specializations.filter(name=specialization).exists() and 
              doctor_info not in ListOfDoctors):
            ListOfDoctors.append(doctor_info)
    ListOfDoctors = sorted(ListOfDoctors, key=lambda x: x.rate, reverse=True)

    return render(request, 'base/doctorlist.html', {'ListOfDoctors': ListOfDoctors})
