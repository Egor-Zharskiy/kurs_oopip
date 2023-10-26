from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from advertisements.models import Car, Image
from common.views import TitleMixin


class StartView(TitleMixin, TemplateView):
    template_name = 'start.html'
    title = "CarSell - Начальная страница"


# to be continued
# class CarsView(TitleMixin, ListView):

def start(request):
    context = {
        'title': "Start page - CarSell"
    }
    return render(request, 'start.html', context)


def post(request):
    return render(request, 'post.html', context={})


def cars(request):
    cars = Car.objects.all()
    data = []
    for car in cars:
        image = Image.objects.filter(car=car).first()
        data.append([car, image])
        print(image)

    context = {
        'cars': cars,
        'title': "CarSell - объявления",
        'data': data,
        'image': image,
    }
    return render(request, 'index.html', context)


def article(request, pk):
    car = Car.objects.get(pk=pk)
    images = Image.objects.filter(car=car)
    print(images)
    context = {
        'car': car,
        'images': images,
    }
    return render(request, 'article.html', context)
