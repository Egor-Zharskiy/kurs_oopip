from django.http import Http404
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, ListView, UpdateView

from advertisements.forms import FilterForm
from advertisements.models import Car, Image, CarBrand, CarModel, CarGeneration
from common.views import TitleMixin


class StartView(TitleMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        if not bool(request.GET):
            return render(request, 'start.html', context={'title': "CarSell - Начальная страница"})

        brand_id = request.GET.get('brand')
        model_id = request.GET.get('model')
        generation_id = request.GET.get('generations')
        release_year = request.GET.get('release_year')
        mileage = request.GET.get('mileage')
        return redirect('index.html', brand=brand_id, model=model_id, generation=generation_id,
                        release_year=release_year, mileage=mileage)


class CarsView(TitleMixin, ListView):
    model = Car
    template_name = "index.html"
    title = 'CarSell - Объявления'

    def get_queryset(self):
        brand_id = self.request.GET.get('brand')
        model_id = self.request.GET.get('model')
        generation_id = self.request.GET.get('generations')
        release_year = self.request.GET.get('release_year')
        mileage = self.request.GET.get('mileage')
        price_from = self.request.GET.get('price_from')
        price_to = self.request.GET.get('price_to')
        print(price_from, 'price_from')
        print(price_to, 'price_to')
        cars = Car.objects.all()

        if brand_id:
            car_brand = CarBrand.objects.get(id=brand_id)
            cars = cars.filter(brand=car_brand)

        if model_id:
            cars = cars.filter(model__id=model_id)

        if generation_id:
            cars = cars.filter(generation__id=generation_id)

        if release_year:
            cars = cars.filter(release_year=release_year)

        if mileage:
            cars = cars.filter(mileage=mileage)

        if price_from:
            cars = cars.filter(price__gte=price_from)

        if price_to:
            cars = cars.filter(price__lte=price_to)

        # print(cars, 'cars')
        queryset = []

        for car in cars:
            # print(car, 'car')
            image = Image.objects.filter(car=car).first()
            queryset.append([car, image])

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        # print(queryset, 'context_data')
        if len(queryset) >= 0:
            context['data'] = queryset
            return context
        # print('using this, renault')
        data = []
        for car in Car.objects.all():
            image = Image.objects.filter(car=car).first()
            data.append([car, image])
        # form = FilterForm()
        # context = super().get_context_data(**kwargs)
        context['data'] = data
        # context['form'] = form

        return context

    # def post(self, request, **kwargs):
    #     if request.method == "POST":
    #         form = FilterForm(request.POST)
    #         if form.is_valid():
    #             queryset = self.get_queryset()
    #             print(queryset)
    #
    #             print(queryset, 'queryset')
    #             context = {
    #                 'data': queryset,
    #                 'form': FilterForm(),
    #             }
    #         else:
    #             queryset = self.get_queryset()
    #             context = {
    #                 'data': queryset,
    #                 'form': FilterForm(),
    #             }
    #         return render(request, 'index.html', context)


class ArticleView(TitleMixin, TemplateView):
    template_name = 'article.html'
    title = 'Объявление'

    def get_context_data(self, pk, **kwargs):
        car = Car.objects.get(pk=pk)
        username_id = car.username_id
        # print(username_id, 'username_id')
        images = Image.objects.filter(car=car)
        context = super().get_context_data(**kwargs)
        context['car'] = car
        context['images'] = images
        context['user_id'] = username_id
        return context