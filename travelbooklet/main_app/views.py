from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from amadeus import Client, ResponseError
import requests
from django.contrib import messages
import json
import os

# Amadeus API
client_id = os.getenv('AMADEUS_API_KEY')
client_secret = os.getenv('AMAEDEUS_API_SECRET')

amadeus = Client(
    client_id = client_id,
    client_secret = client_secret
)

# Get access token
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}

data = {
  'grant_type': 'client_credentials',
  'client_id': client_id,
  'client_secret': client_secret
}

response = requests.post('https://test.api.amadeus.com/v1/security/oauth2/token', headers=headers, data=data)

print(response.json())
token = response.json()
print(token['access_token'])

# Call API
headers = {
    'Authorization': f'Bearer {token["access_token"]}',
}

params = (
    ('origin', 'PAR'),
    ('maxPrice', '200'),
)


response = requests.get('https://test.api.amadeus.com/v1/shopping/flight-destinations', headers=headers, params=params)

print(response.json())


# Create your views here.
def home(request):
    return render(request,'home.html')

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