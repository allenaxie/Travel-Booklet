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
    notes = models.TextField(max_length=400)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('trips_index')