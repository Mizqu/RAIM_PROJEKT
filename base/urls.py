from django.urls import path
from base.views import index
from base.views import login_view, register_view, logout_view, show_profile
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from . import views


urlpatterns = [
    path('', index, name="index"),
    path('login/', login_view, name='login'),
    path('register/', register_view, name="register"),
    path('logout/', logout_view, name='logout'),
    path('profile/', show_profile, name='profile' )
]