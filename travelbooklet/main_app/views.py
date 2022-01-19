from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from amadeus import Client, ResponseError
import requests
from django.contrib import messages
import json
import os
import random #random.choices()
import re # regex

# Amadeus API keys
client_id = os.getenv('AMADEUS_API_KEY')
client_secret = os.getenv('AMAEDEUS_API_SECRET')

amadeus = Client(
    client_id = client_id,
    client_secret = client_secret
)

# Create your views here.
def home(request):


    # # ------------------ Amadeus API --------------------
    # # Get Amadeus API access token
    # headers = {
    #     'Content-Type': 'application/x-www-form-urlencoded',
    # }
    # data = {
    # 'grant_type': 'client_credentials',
    # 'client_id': client_id,
    # 'client_secret': client_secret
    # }
    # response = requests.post('https://test.api.amadeus.com/v1/security/oauth2/token', headers=headers, data=data)
    # token = response.json()
    # # Call API - travel recommendation
    # headers = {
    #     'Authorization': f'Bearer {token["access_token"]}',
    # }
    # params = (
    #     ('cityCodes', f'{random.choice(iata_array)}'),
    # )
    # response = requests.get('https://test.api.amadeus.com/v1//reference-data/recommended-locations', headers=headers, params=params)
    # data= response.json()
    # print('featured city',data["data"][0]["name"])



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

def trips(request):
    return render(request, 'trips/index.html')