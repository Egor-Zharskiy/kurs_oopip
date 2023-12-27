from django.contrib import admin

from users.models import User
from advertisements.models import Car, Image, CarModel, CarBrand, CarGeneration

admin.site.register(User)
admin.site.register(Image)
admin.site.register(CarBrand)
admin.site.register(CarModel)
admin.site.register(CarGeneration)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'username', 'price', 'created_timestamp')