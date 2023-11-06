from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, ListView

from advertisements.forms import FilterForm
from advertisements.models import Car, Image
from common.views import TitleMixin


class StartView(TitleMixin, TemplateView):
    template_name = 'start.html'
    title = "CarSell - Начальная страница"


class CarsView(TitleMixin, ListView):
    model = Car
    template_name = "index.html"
    title = 'CarSell - Объявления'

    def get_queryset(self):
        print(self.request.method, 'method')
        min_price = self.request.POST.get('min_price')
        max_price = self.request.POST.get('max_price')
        queryset = []
        for car in Car.objects.all():
            image = Image.objects.filter(car=car).first()
            queryset.append([car, image])

        if min_price and max_price:
            queryset = []
            print(Car.objects.filter(price__range=(min_price, max_price)))
            for car in Car.objects.filter(price__range=(min_price, max_price)):
                image = Image.objects.filter(car=car).first()
                queryset.append([car, image])
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        data = []
        for car in Car.objects.all():
            image = Image.objects.filter(car=car).first()
            data.append([car, image])
        form = FilterForm()
        context = super().get_context_data(**kwargs)
        context['data'] = data
        context['form'] = form

        return context

    def post(self, request, **kwargs):
        if request.method == "POST":
            form = FilterForm(request.POST)
            if form.is_valid():
                queryset = self.get_queryset()
                print(queryset)

                print(queryset, 'queryset')
                context = {
                    'data': queryset,
                    'form': FilterForm(),
                }
            else:
                queryset = self.get_queryset()
                context = {
                    'data': queryset,
                    'form': FilterForm(),
                }
            return render(request, 'index.html', context)

    # def get(self, request, **kwargs):
        # return render(request, 'index.html')


class ArticleView(TemplateView):
    template_name = 'article.html'

    def get_context_data(self, pk, **kwargs):
        car = Car.objects.get(pk=pk)
        username_id = car.username_id
        print(username_id)
        images = Image.objects.filter(car=car)
        context = super().get_context_data(**kwargs)
        context['car'] = car
        context['images'] = images
        context['user_id'] = username_id
        return context

# def article(request, pk):
#     car = Car.objects.get(pk=pk)
#     images = Image.objects.filter(car=car)
#     print(images)
#     context = {
#         'car': car,
#         'images': images,
#     }
#     return render(request, 'article.html', context)


# to be continued
# class CarsView(TitleMixin, ListView):

#
# def cars(request):
#     cars = Car.objects.all()
#     data = []
#     for car in cars:
#         image = Image.objects.filter(car=car).first()
#         data.append([car, image])
#         # print(image)
#
#     context = {
#         'cars': cars,
#         'title': "CarSell - объявления",
#         'data': data,
#         'image': image,
#     }
#     return render(request, 'index.html', context)
