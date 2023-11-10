from datetime import datetime

from django.db import models

from users.models import User


class CarBrand(models.Model):
    brand = models.CharField(max_length=100)

    def __str__(self):
        return self.brand


class CarModel(models.Model):
    brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE)
    model = models.CharField(max_length=100)

    def get_model(self):
        return self.model

    def __str__(self):
        return f'{self.model}'


class CarGeneration(models.Model):
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    generation = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.generation}'


class Car(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE)
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE, default=None)
    generation = models.ForeignKey(CarGeneration, on_delete=models.CASCADE, default=None)
    release_year = models.IntegerField(default=0)
    mileage = models.IntegerField(default=0)
    color = models.CharField(default='black')
    created_timestamp = models.DateTimeField(auto_now_add=True)

    description = models.TextField()
    price = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f'{self.brand} {self.model} by: {self.username}'


class Image(models.Model):
    car = models.ForeignKey(Car, default=None, on_delete=models.CASCADE)
    images = models.ImageField(upload_to="images/")

    def __str__(self):
        return f'{self.car.brand} {self.car.model} by: {self.car.username}'
