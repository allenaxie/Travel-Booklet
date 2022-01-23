from django import forms
from django.forms import ModelForm
from .models import *

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['username','first_name','last_name','email','birthdate']
