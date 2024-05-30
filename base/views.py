from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from .customfunctions import split_name
from .forms import CustomUserCreationForm, CustomAuthenticationForm, DoctorCreationForm, MessageForm
from .models import Specialization, Message, DoctorInfo
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
User = get_user_model()

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

# Wylogowywanie użytkownika
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

# Okno listy czatów
@login_required
def chat_list(request):
    user = request.user

    # Pobieramy wszystkie unikalne konwersacje, w których uczestniczy użytkownik
    friends = user.friends.all()

    # Tworzymy listę czatów, gdzie każdy czat zawiera nazwę przyjaciela
    return render(request, 'base/chat_list.html', {'friends': friends})

# Okno czatu
@login_required
def chat(request, recipient=None):
    user = request.user
    # Przypisujemy odpowiedniego autora, odbiorcę, treść wiadomości i plik
    if request.method == 'POST':
        author = request.POST.get('author')
        recipient = request.POST.get('recipient')
        content = request.POST.get('content', '')
        file = request.FILES.get('file')

        # Tworzenie nowej wiadomości
        message = Message(author=author, recipient=recipient, content=content, timestamp=timezone.now(), file=file)
        message.save()
        return redirect('chat_with_recipient', recipient=recipient)

    # Wyświetlanie jedynie tych wiadomości, w których aktualny użytkownik jest autorem lub odbiorcą
    messages = Message.objects.filter(
        (Q(author=request.user) & Q(recipient=recipient)) |
        (Q(author=recipient) & Q(recipient=request.user))
    ).order_by('timestamp')  # Wyświetlanie wiadomości posortowanych według czasu wysłania
    return render(request, 'base/chat.html', {'messages': messages, 'recipient': recipient})

# Okno "Kim jesteśmy"
def about(request):
    if request.method == 'GET':
        return render(request, 'base/aboutus.html')
    
@csrf_exempt
def start_conversation(request):
    if request.method == 'POST':
        current_user = request.user
        doctor_id = request.POST.get('user_id')
        doctor = User.objects.get(pk=doctor_id)
        current_user.friends.add(doctor)
        current_user.save()
        return redirect(reverse('chat_list'))
    return redirect('base/chat.html')
