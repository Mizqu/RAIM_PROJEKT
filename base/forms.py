from django import forms
from .models import DoctorInfo
from django.contrib.auth.forms import UserCreationForm
from .models import User, Specialization
from django.contrib.auth.forms import AuthenticationForm
import json

class DoctorInputForm(forms.Form):
    specializations = forms.ModelMultipleChoiceField(
        queryset=Specialization.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    class Meta:
        model = DoctorInfo
        fields = ['specializations']

    def save(self, commit=True):
        instance = super().save(commit=False)
        specializations = self.cleaned_data.get('specializations', [])
        instance.specializations = json.dumps([spec.id for spec in specializations])
        if commit:
            instance.save()
        return instance

    

class CustomUserCreationForm(forms.ModelForm):
    username = forms.CharField(label='Nazwa użytkownika')
    password1 = forms.CharField(label='Hasło', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Potwierdź hasło', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
  
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data["password1"]
        if commit:
            user.set_password(password)
            user.save()
        return user    
#bez tego użytkownik tworzy się, ale nie nadawane jest mu hasło
    
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Nazwa użytkownika')
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'password']
        