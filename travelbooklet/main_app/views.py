from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from amadeus import Client, ResponseError
import requests
from django.contrib import messages
import json
import os
import random

# Amadeus API keys
client_id = os.getenv('AMADEUS_API_KEY')
client_secret = os.getenv('AMAEDEUS_API_SECRET')

amadeus = Client(
    client_id = client_id,
    client_secret = client_secret
)

# Create your views here.
def home(request):
    iata_array = [
        # France
        'CDG','NCE',
        # Spain
        'MAD','BCN',
        # Italy
        'FCO','MXP','VCE',
        # Germany
        'FRA','TXL',
        # United Kingdom
        'LHR','LGW',
        # America
        'ATL','LAX','ORD','DFW','JFK','SFO','SEA','LAS','MIA','HNL','SAN',
        # Mexico
        'MEX','CUN','GDL','TIJ',
        # Saudi Arabia
        'JED','RUH',
        # Netherlands
        'AMS','EIN',
    ]
    # Get Amadeus API access token
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret
    }
    response = requests.post('https://test.api.amadeus.com/v1/security/oauth2/token', headers=headers, data=data)
    token = response.json()
    # Call API - travel recommendation
    headers = {
        'Authorization': f'Bearer {token["access_token"]}',
    }
    params = (
        ('cityCodes', f'{random.choice(iata_array)}'),
    )
    response = requests.get('https://test.api.amadeus.com/v1//reference-data/recommended-locations', headers=headers, params=params)
    data= response.json()
    print('featured city',data["data"][0]["name"])
    # Imsea Image search API - 3 relevant destinations
    image1 = requests.get(f'https://imsea.herokuapp.com/api/1?q={data["data"][0]["name"]}').json()
    image2 = requests.get(f'https://imsea.herokuapp.com/api/1?q={data["data"][1]["name"]}').json()
    image3 = requests.get(f'https://imsea.herokuapp.com/api/1?q={data["data"][2]["name"]}').json()
    # Render home page
    return render(request,'home.html',{
        'data':data,
        'image1':image1,
        'image2':image2,
        'image3':image3
        })

def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Add user to database
            user = form.save()
            # log in the user
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)