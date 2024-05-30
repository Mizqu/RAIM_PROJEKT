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
        if form.is_valid(): # specjalizacje wybrane przez użytkownika (przyszłego lekarza) są wyciągane z formularza, jego przekonywujący tekst również i na tej podstawie 
            specializations = form.cleaned_data['specializations']  # tworzona jest prośba o możliwość zostania lekarzem która ląduje w bazie danych i admin ją zatwierdza bądź nie
            encouragement = form.cleaned_data['encouragement']
            doctor_info = DoctorInfo.objects.create(user_id=request.user.id, encouragement=encouragement)
            doctor_info.specializations.set(specializations)           
            doctor_info.save()
            return redirect('index')
    else:
        form = DoctorCreationForm()
    context = {
        'form': form, # pobierane są z bazy danych wszystkie specjalizacje  i wysyłane do contextu który przekazywany jest do widoku, jest to po to aby w modalu wyświetlić
        'Specializations': Specialization.objects.all() # wszystkie możliwe specjalizacje przy rejestracji lekarza
    }
    return render(request, 'base/index.html', context)


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST) # formularz ktory jest w widoku login.html przekazywany jest do tej metody
        if form.is_valid():
            username = form.cleaned_data.get('username') # pobierane są username, password i użytkownik jest logowany
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user) # jeśli autentykacja powiedzie się użytkownik przekierowywany jest na index.html
                return redirect(reverse('index'))   
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == 'POST': # formularz ktory jest w widoku register.html przekazywany jest do tej metody
        form = CustomUserCreationForm(request.POST)
        if form.is_valid(): # jesli dane z inputów w register.html odpowiadają typom danych z formularza to użytkownik jest tworzony i zapisywany do bazy danych, następnie wraca do index.html
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
    user = request.user # jeśli użytkownik wykonujący request pokazania profilu jest lekarzem to flaga doctorctx jest true i przekazywany jest odpowiedni kontekst tak aby można 
    if user.isDoctor:                                   # było pobrać dodatkowo specjalizacje i bio lekarza
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
        full_name = request.GET.get('full_name') # Użytkownik może wpisać imie i nazwisko lekarza i/lub wybiera specjalizacje która go interesuje, następnie full_name jest dzielone 
        specialization = request.GET.get('specialization') # na first_name i last_name a następnie szukani są w bazie danych lekarze którzy mają podany first_name last_name i specjalizacje
        first_name, last_name = split_name(full_name) # dodawani są do listy i przekazywani do widoku
    ListOfDoctors = []
    for doctor_info in DoctorInfo.objects.filter(approved=True):
        if doctor_info.user.first_name == first_name and doctor_info.user.last_name == last_name:
            ListOfDoctors.append(doctor_info)
        elif (doctor_info.specializations.filter(name=specialization).exists() and 
              doctor_info not in ListOfDoctors):
            ListOfDoctors.append(doctor_info)
    ListOfDoctors = sorted(ListOfDoctors, key=lambda x: x.rate, reverse=True)

    return render(request, 'base/doctorlist.html', {'ListOfDoctors': ListOfDoctors})

@login_required
def chat_list(request):
    user = request.user

    # Pobieramy wszystkie unikalne konwersacje, w których uczestniczy użytkownik
    friends = user.friends.all()

    # Tworzymy listę czatów, gdzie każdy czat zawiera nazwę przyjaciela


    return render(request, 'base/chat_list.html', {'friends': friends})

@login_required
def chat(request, recipient=None):
    user = request.user
    if request.method == 'POST':
        author = request.POST.get('author')
        recipient = request.POST.get('recipient')
        content = request.POST.get('content', '')
        file = request.FILES.get('file')

        message = Message(author=author, recipient=recipient, content=content, timestamp=timezone.now(), file=file)
        message.save()
        return redirect('chat_with_recipient', recipient=recipient)

    messages = Message.objects.filter(author=user.username) | Message.objects.filter(recipient=user.username)
    messages = messages.order_by('timestamp')
    return render(request, 'base/chat.html', {'messages': messages, 'recipient': recipient})



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
