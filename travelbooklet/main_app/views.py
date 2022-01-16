from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from amadeus import Client, ResponseError


amadeus = Client(
    client_id='GF2UH9WOwXfNmLSSYsyyBeawJr5ghrcY',
    client_secret='33XFwDCnrKpaygAD'
)

# Create your views here.
def home(request):
    print('hi')
    try:
        response = amadeus.reference_data.urls.checkin_links.get(airlineCode='BA')
        data = response.data
        print(data)
    except ResponseError as error:
        print(error) 
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