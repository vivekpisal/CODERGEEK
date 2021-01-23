from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django import forms


class InfoForm(ModelForm):
	class Meta:
		model=Info
		fields=["name","profile","college","github","linkdln"]

class RegisterForm(UserCreationForm):
	email=forms.EmailField()
	class Meta:
		model=User
		fields=["username","email","password1","password1"]


class SignUpForm(UserCreationForm):
	email = forms.EmailField(label = ("Email"))

	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2')
