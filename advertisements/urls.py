from django.contrib import admin
from django.urls import path
from advertisements.views import StartView, CarsView, ArticleView

app_name = "advertisements"

urlpatterns = [
    path('', StartView.as_view(), name='start'),
    path('cars/', CarsView.as_view(), name='cars'),
    path('article/<int:pk>', ArticleView.as_view(), name='article')
]
