from django.urls import path
from users.views import (profile,
                         logout, GetModels,
                         get_car_brands, get_generations, demo_post, GetModelsView, GetGenerationsView,
                         EditCarView, DeleteCarView, LoginUser, Registration, ProfileView)  # , login, registration

app_name = 'users'
urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('registration/', Registration.as_view(), name='registration'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('logout/', logout, name='logout'),
    path('create_post/', demo_post, name='create_post'),
    path('get_models/', GetModels.as_view(), name='get_models'),
    path('get_car_brands/', get_car_brands, name='get_car_brands'),
    path('get_generations/', get_generations, name='get_generations'),
    path('update_models/', GetModelsView.as_view(), name='update_models'),
    path('update_generations/', GetGenerationsView.as_view(), name='update_generations'),
    path('edit/<int:pk>', EditCarView.as_view(), name='edit_car'),
    path('delete_car/<int:pk>', DeleteCarView.as_view(), name='delete_car'),
]
