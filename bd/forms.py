from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput

from .models import Authors, Courses


class AuthorsForm(ModelForm):
    class Meta:
        model = Authors
        fields = ['id_user', 'surname', 'name', 'email']
        widgets = {
            "id_user": TextInput(attrs={'type': 'hidden'})
        }


class CourseForm(ModelForm):
    class Meta:
        model = Courses
        fields = ['header', 'description', 'main_text', 'start_date', 'end_date',  'id_author']
        widgets = {
            "id_author": TextInput(attrs={'type': 'hidden'})
        }


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'placeholder': "ИМЯ ПОЛЬЗОВАТЕЛЯ"}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'placeholder': "ПАРОЛЬ"}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'placeholder': " ПОВТОР ПАРОЛЯ"}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        widgets = {
            "username": forms.TextInput(attrs={'placeholder': "ИМЯ ПОЛЬЗОВАТЕЛЯ"}),
            "password1": forms.PasswordInput(attrs={'placeholder': "ПАРОЛЬ"}),
            "password2": forms.PasswordInput(attrs={'placeholder': "ПОВТОР ПАРОЛЯ"})
        }


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'placeholder': "ИМЯ ПОЛЬЗОВАТЕЛЯ"}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'placeholder': "ПАРОЛЬ"}))
