from datetime import datetime
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib import auth
from django.views import View
from django.views.generic import UpdateView, DeleteView, TemplateView, DetailView

from advertisements.models import Car, Image, CarBrand, CarModel, CarGeneration
from common.views import TitleMixin
from users.forms import UserRegistrationForm, UserLoginForm, UserProfileForm, PostCreationForm, ImageCreationForm, \
    CarForm, CarEditForm
from users.models import User

from django.core import serializers


# def login(request):
#     if request.method == "POST":
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             print(username, password)
#             user = auth.authenticate(username=username, password=password)
#             auth.login(request, user)
#             return HttpResponseRedirect(reverse('advertisements:cars'))
#         else:
#             print(form.errors, 'form is not valid')
#             messages.error(request, 'Все поля должны быть заполнены корректно.')
#     else:
#         form = UserLoginForm()
#
#     context = {'form': form}
#
#     return render(request, "login.html", context)


class LoginUser(TitleMixin, View):
    template_name = 'login.html'
    title = 'Авторизация'

    def get(self, request):
        form = UserLoginForm()
        context = {
            'form': form,
            'title': "CarSell - Авторизация",
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('advertisements:cars'))
        print(form.errors)
        context = {
            'form': form,
            'title': "CarSell - Авторизация",
        }
        return render(request, self.template_name, context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('advertisements:cars'))


# def registration(request):
#     if request.method == "POST":
#         form = UserRegistrationForm(data=request.POST)
#
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('advertisements:cars'))
#
#     else:
#         form = UserRegistrationForm()
#
#     context = {'form': form}
#
#     return render(request, "registration.html", context)


class Registration(TitleMixin, View):
    template_name = 'registration.html'

    def get(self, request):
        form = UserRegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print(request.POST)
            form.save()
            # login(request, user)
            return HttpResponseRedirect(reverse('advertisements:cars'))

        return render(request, self.template_name, {'form': form})


def profile(request, pk):
    context = {}
    if not pk:
        form = UserProfileForm(instance=request.user)
        advertisements = Car.objects.filter(username=request.user)
        context['user_id'] = request.user.id
        print(request.user.id, 'request.user.id')
    else:
        print(request.user.id, 'else')
        form = UserProfileForm(instance=User.objects.get(pk=pk))
        advertisements = Car.objects.filter(username=User.objects.get(pk=pk))
    context['form'] = form

    owner_id = advertisements.first().username.id if advertisements else 0
    # проверить, не пусто ли количество объявлений продавца
    # owner_id = advertisements.first().username.id
    print(owner_id, 'owner_id')

    context['advertisements'] = advertisements
    context['user_id'] = owner_id
    print(owner_id)

    return render(request, 'profile.html', context=context)


class ProfileView(View):
    template_name = 'profile.html'
    model = User

    # template_name = 'profile.html'

    def get(self, request, pk=None):
        # Если pk не передан, используем id текущего пользователя
        if not pk:
            pk = request.user.id

        user = get_object_or_404(User, pk=pk)
        form = UserProfileForm(instance=user)
        advertisements = Car.objects.filter(username=user)
        owner_id = advertisements.first().username.id if advertisements else 0

        # Проверяем, является ли текущий пользователь тем, чей профиль просматривается
        is_owner = request.user.id == owner_id

        context = {
            'form': form,
            'advertisements': advertisements,
            'user_id': owner_id,
            'is_owner': is_owner,
        }

        return render(request, self.template_name, context)
    # def get(self, pk, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     pk = self.kwargs.get('pk')
    #     print(pk, 'pk')
    #     context['form'] = UserProfileForm(instance=User.objects.get(pk=pk))
    #     advertisements = Car.objects.filter(username=User.objects.get(pk=pk))
    #     owner_id = advertisements.first().username.id if advertisements else 0
    #     context['advertisements'] = advertisements
    #     context['user_id'] = owner_id
    #     visibility = 1 if owner_id == self.request.user.id else 0
    #     print(visibility, 'visibility')
    #     context['visibility'] = visibility
    #     print(owner_id, 'owner_id')
    #     print(self.request.user.id, 'self.request.user.id')
    #     return context


class GetModels(View):
    def get(self, request):
        brand_id = request.GET.get('brand_id')
        print(brand_id)
        if brand_id is not None:
            models = CarModel.objects.filter(brand=brand_id)
            model_data = [{'id': model.id, 'name': model.get_model()} for model in models]
            print(model_data)
            return JsonResponse({'models': model_data})
        else:
            return JsonResponse({'error': 'Выберите бренд'}, status=400)


def get_car_brands(request):
    car_brands = CarBrand.objects.all()
    data = {'brands': [{'id': brand.id, 'name': brand.brand} for brand in car_brands]}
    return JsonResponse(data)


def get_generations(request):
    model_id = request.GET.get('model_id')
    if model_id is not None:
        generations = CarGeneration.objects.filter(model=model_id)
        # print(generations)
        data = [{'id': generation.id, 'name': generation.generation} for generation in generations]
        # print(data)
        return JsonResponse({'generations': data})


def demo_post(request):
    print(request.POST)
    if request.method == "POST":
        car = Car.objects.create(username=request.user, brand=CarBrand.objects.get(id=request.POST['brand']),
                                 model=CarModel.objects.get(id=request.POST['model']),
                                 generation=CarGeneration.objects.get(id=request.POST['generations']),
                                 release_year=request.POST['release_year'], mileage=request.POST['mileage'],
                                 color=request.POST['mileage'], description=request.POST['description'],
                                 price=request.POST['price'])
        car.save()

        for f in request.FILES.getlist('photos'):
            print(f)
            data = f.read()
            image = Image.objects.create(car=car, images=f)
            image.save()
        return redirect(reverse('advertisements:cars'))

    print(request.FILES, 'files')

    return render(request, 'create_post.html', context={})


# class CarUpdateView(UpdateView):
#     model = Car
#     form_class = EditCar
#     template_name = 'edit_post.html'
#     success_url = reverse_lazy('advertisements:cars')
#
#     def get_object(self, queryset=None):
#         car_id = self.kwargs.get('car_id')
#         return get_object_or_404(Car, id=car_id)


class GetModelsView(View):
    def get(self, request, *args, **kwargs):
        brand_id = self.request.GET.get('brand_id')
        models = CarModel.objects.filter(brand_id=brand_id)
        data = serializers.serialize('json', models)
        return JsonResponse({'models': data}, safe=False)


class GetGenerationsView(View):
    def get(self, request, *args, **kwargs):
        model_id = self.request.GET.get('model_id')
        generations = CarGeneration.objects.filter(model_id=model_id)
        data = serializers.serialize('json', generations)
        return JsonResponse({'generations': data}, safe=False)


class EditCarView(TitleMixin, UpdateView):
    model = Car
    form_class = CarEditForm
    template_name = 'edit_post.html'
    title = "CarSell - Редактирование объявления"

    def get_success_url(self):
        user_profile_url = reverse('users:profile', kwargs={'pk': self.request.user.id})

        return user_profile_url


class DeleteCarView(View):

    def get(self, request, pk):
        car = get_object_or_404(Car, pk=pk)

        car.delete()

        return HttpResponseRedirect(reverse('users:profile', kwargs={'pk': request.user.id}))
