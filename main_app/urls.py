from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/',views.signup, name='signup'),
    path('trips/', views.trips_index, name='trips_index'),
    path('trips/create', views.TripCreate.as_view(), name="trips_create"),
]