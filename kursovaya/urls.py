
from django.contrib import admin
from django.urls import path, include
from advertisements.views import start

urlpatterns = [
    path('', include('advertisements.urls', namespace='advertisements')),
    path('admin/', admin.site.urls),
]
