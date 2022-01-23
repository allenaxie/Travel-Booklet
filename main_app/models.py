from django.db import models
from django.urls import reverse 
from datetime import date
from django.contrib.auth.models import User

# Create your models here.
class Trip(models.Model):
    name = models.CharField('Trip Name', max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    departure_location = models.CharField(max_length=100)
    destination = models.CharField(max_length = 100)
    notes = models.TextField(max_length=400, blank=True, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('trips_index')

class Profile(models.Model):
    username = models.CharField(max_length=25, unique=True)
    first_name = models.CharField('First name', max_length=50, blank=True, null=True)
    last_name = models.CharField('Last name', max_length=50, blank=True, null=True)
    email = models.CharField('Email', max_length=100, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('profile')
    
