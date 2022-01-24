from django import forms
from django.forms import ModelForm
from .models import Trip

class InspForm(forms.Form):
    depart_city = forms.CharField(max_length=3)
