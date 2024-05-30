from django import forms
from .models import User, Specialization, DoctorInfo, Message
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
import json

class DoctorCreationForm(forms.Form):
    specializations = forms.ModelMultipleChoiceField(
        queryset=Specialization.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    encouragement = forms.CharField(widget=forms.Textarea)

class CustomUserCreationForm(forms.ModelForm):
    first_name = forms.CharField(label='Imie:  ')
    last_name = forms.CharField(label='Nazwisko:  ')
    username = forms.CharField(label='Nazwa użytkownika:  ')
    password1 = forms.CharField(label='Hasło:  ', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Potwierdź hasło:  ', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'password1', 'password2']
  
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

# Formularz wiadomości
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['author', 'recipient', 'content', 'file'] # Pola na autora, odbiorcę, zawartość i plik
        widgets = {
            'author': forms.HiddenInput(),  # Do autora nie można nic wpisać - autorem zawsze jest aktualnie zalogowany użytkownik
            'recipient': forms.HiddenInput, # Tak samo do odbiorcy, odbiorcę wybiera się z listy - nie powinno się go ręcznie wpisywać
            'content': forms.TextInput(attrs={'placeholder': 'Treść wiadomości'}),  # Zawartość
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(MessageForm, self).__init__(*args, **kwargs)
        if self.user:
            self.initial['author'] = self.user  # Autorem jest użytkownik