from django.urls import path
from base.views import index
from base.views import login_view, register_view, logout_view, show_profile, doctorSearch, chat, about, start_conversation
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from . import views

# Wszystkie podstrony
urlpatterns = [
    path('', index, name="index"),
    path('login/', login_view, name='login'),
    path('register/', register_view, name="register"),
    path('logout/', logout_view, name='logout'),
    path('profile/', show_profile, name='profile' ),
    path('doctor_search/', doctorSearch, name='doctor_search'),
    
    path('chat/', chat, name='chat'),
    path('list/', views.chat_list, name='chat_list'),
    path('chat/<str:recipient>/', views.chat, name='chat_with_recipient'),
    
    path('about/', about, name='about'),
    path('start_conversation/', start_conversation, name='start_conversation')
]