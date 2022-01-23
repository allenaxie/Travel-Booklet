from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from amadeus import Client, ResponseError
import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import json
import os
import random #random.choices()
import re # regex
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
import uuid
import boto3
import os
from .models import *


# Amadeus API keys
client_id = os.getenv('AMADEUS_API_KEY')
client_secret = os.getenv('AMAEDEUS_API_SECRET')

amadeus = Client(
    client_id = client_id,
    client_secret = client_secret
)

# Create your views here.
def home(request):

    # -------------- Teleport API --------------
    # Access list of urban areas
    urban_areas = requests.get('https://api.teleport.org/api/urban_areas/').json()['_links']['ua:item']

    # Choose 3 random ones from list and add to array
    random_area_list = random.choices(urban_areas, k=3)
    data_array = []

    # Call Teleport API and fetch info
    for idx, city in enumerate(random_area_list):
        city_info = requests.get(f'https://api.teleport.org/api/cities/?search={city["name"]}&embed=city%3Asearch-results%2Fcity%3Aitem%2Fcity%3Aurban_area%2Fua%3Ascores').json()
        
        city_scores = (city_info['_embedded']['city:search-results'][0]['_embedded']['city:item']['_embedded']['city:urban_area']['_embedded']['ua:scores']['categories']) 
        city_summary = (city_info['_embedded']['city:search-results'][0]['_embedded']['city:item']['_embedded']['city:urban_area']['_embedded']['ua:scores']['summary'])
        city_country = (city_info['_embedded']['city:search-results'][0]['_embedded']['city:item']['_embedded']['city:urban_area']['_links']['ua:countries'][0]['name'])
        
        city_image_links = (city_info['_embedded']['city:search-results'][0]['_embedded']['city:item']['_embedded']['city:urban_area']['_links']['ua:images']['href'])
        city_image = requests.get(city_image_links).json()['photos'][0]['image']

        city_full_name= (city_info['_embedded']['city:search-results'][0]['_embedded']['city:item']['_embedded']['city:urban_area']['full_name'])
        data_array.extend([[city_full_name, city_country, city_image, city_scores, city_summary]])
    
    # Render home page
    return render(request,'home.html',{
        'data': data_array
        })

def signup(request, backend='allauth.account.auth_backends.AuthenticationBackend'):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Add user to database
            user = form.save()
            # log in the user
            login(request, user, backend = 'allauth.account.auth_backends.AuthenticationBackend')
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


# Trips
@login_required
def trips_index(request):
    trips = Trip.objects.filter(user = request.user)
    return render(request, 'trips/index.html',{'trips': trips})


class TripCreate(LoginRequiredMixin, CreateView):
    model = Trip
    fields = ["name", "start_date", "end_date", "departure_location", "destination", "notes"]

    def form_valid(self, form):
        # Assign the logged in user as owner of the Cat being created
        form.instance.user = self.request.user
        # Let the CreateView do its job as usual
        return super().form_valid(form)
    
class TripUpdate(LoginRequiredMixin, UpdateView):
    model = Trip
    fields = ["name", "start_date", "end_date", "departure_location", "destination", "notes"]

    def get(self, request, pk):
        self.object = self.get_object()
        if self.object.user == self.request.user:
            return super().get(self, request, pk)
        else:
            return redirect('/trips/')

    def post(self, request, pk):
        self.object = self.get_object()
        if self.object.user == self.request.user:
            return super().post(self, request, pk)
        else:
            return redirect('/trips/')


def trips_delete(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    trip.delete()
    return redirect('trips_index')
