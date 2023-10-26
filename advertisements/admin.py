from django.contrib import admin

from users.models import User
from advertisements.models import Car, Image

admin.site.register(User)
admin.site.register(Image)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'username', 'price', 'created_timestamp')
    # fields = ('name', 'description', ('price', 'quantity'), 'image', 'category')
    # readonly_fields = ('description',)
    # search_fields = ('name',)
    # ordering = ('-name',)
