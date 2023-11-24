from django.contrib import admin
from django.urls import path
from advertisements.views import StartView, CarsView, ArticleView
from users.views import GetModels, get_car_brands, get_generations

app_name = "advertisements"

urlpatterns = [
    path('', StartView.as_view(), name='start'),
    path('cars/', CarsView.as_view(), name='cars'),
    path('article/<int:pk>', ArticleView.as_view(), name='article'),
    path('get_models/', GetModels.as_view(), name='get_models'),
    path('get_car_brands/', get_car_brands, name='get_car_brands'),
    path('get_generations/', get_generations, name='get_generations'),
]
