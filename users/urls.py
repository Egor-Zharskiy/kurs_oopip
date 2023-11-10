from django.urls import path
from users.views import (registration, profile, login,
                         logout, create_post, GetModels,
                         get_car_brands, get_generations, demo_post)

app_name = 'users'
urlpatterns = [
    path('login/', login, name='login'),
    path('registration/', registration, name='registration'),
    path('profile/<int:pk>', profile, name='profile'),
    path('logout/', logout, name='logout'),
    path('create_post/', demo_post, name='create_post'),
    path('get_models/', GetModels.as_view(), name='get_models'),
    path('get_car_brands/', get_car_brands, name='get_car_brands'),
    path('get_generations/', get_generations, name='get_generations'),

]
