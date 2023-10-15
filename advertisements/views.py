from django.shortcuts import render
from django.views.generic import TemplateView, ListView
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


def cars(request):
    context = {
        'title': "CarSell - объявления"
    }

    return render(request, 'index.html', context)
