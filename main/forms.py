from django.forms import ModelForm
from .models import *


class InfoForm(ModelForm):
	class Meta:
		model=Info
		fields=["name","profile","college","github","linkdln"]

