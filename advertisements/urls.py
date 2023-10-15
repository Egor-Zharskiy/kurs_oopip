from django.contrib import admin
from django.urls import path
from advertisements.views import start, cars, StartView

app_name = "advertisements"

urlpatterns = [
    path('', StartView.as_view(), name='start'),
    path('cars/', cars, name='cars')
]
