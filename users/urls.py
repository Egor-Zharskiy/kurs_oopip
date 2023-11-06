from django.urls import path
from users.views import registration, profile, login, logout, create_post

app_name = 'users'
urlpatterns = [
    path('login/', login, name='login'),
    path('registration/', registration, name='registration'),
    path('profile/<int:pk>', profile, name='profile'),
    path('logout/', logout, name='logout'),
    path('create_post/', create_post, name='create_post')

]
