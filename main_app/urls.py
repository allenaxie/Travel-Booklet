from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Flights
    path('flights/',views.flights_index, name="flights_index"),

    # Sign up
    path('accounts/signup/',views.signup, name='signup'),



    # Trips
    path('trips/', views.trips_index, name='trips_index'),
    path('trips/create', views.TripCreate.as_view(), name="trips_create"),
    path('trips/<int:pk>/update/', views.TripUpdate.as_view(), name="trips_update"),
    path('trips_delete/<int:trip_id>/', views.trips_delete, name="trips_delete"),
]