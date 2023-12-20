from datetime import datetime
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin

from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib import auth
from django.views import View
from django.views.generic import UpdateView, DeleteView, TemplateView, DetailView
from django.views.generic.edit import CreateView

from advertisements.models import Car, Image, CarBrand, CarModel, CarGeneration
from common.views import TitleMixin
from users.forms import UserRegistrationForm, UserLoginForm, UserProfileForm, PostCreationForm, ImageCreationForm, \
    CarForm, CarEditForm, UserProfileEditForm
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


class ProfileView(View):
    template_name = 'profile.html'
    model = User

    def get(self, request, pk=None):
        print(request.path)
        if not pk:
            pk = request.user.id
        print(pk, self.request.user.id)

        user = get_object_or_404(User, pk=pk)
        form = UserProfileForm(instance=user)
        advertisements = Car.objects.filter(username=user)
        owner_id = advertisements.first().username.id if advertisements else 0

        # is_owner = request.user.id == owner_id
        is_owner = self.request.user.id == pk
        context = {
            'form': form,
            'advertisements': advertisements,
            'user_id': owner_id,
            'is_owner': is_owner,
        }

        return render(request, self.template_name, context)


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


class CreateCarView(CreateView):
    model = Car
    form_class = CarEditForm
    template_name = 'create_post.html'
    success_url = '/advertisements/cars/'

    def get(self, request, *args, **kwargs):
        return render(request, 'create_post.html', context={})

    def post(self, request, *args, **kwargs):
        print(self.request.POST, 'request')

        # response = super().form_valid(form)

        car = Car.objects.create(username=self.request.user, brand=CarBrand.objects.get(id=self.request.POST['brand']),
                                 model=CarModel.objects.get(id=self.request.POST['model']),
                                 generation=CarGeneration.objects.get(id=self.request.POST['generations']),
                                 release_year=self.request.POST['release_year'], mileage=self.request.POST['mileage'],
                                 color=self.request.POST['mileage'], description=self.request.POST['description'],
                                 price=self.request.POST['price'])
        car.save()
        print(car, 'carcarcar')
        multiple_images = self.request.FILES.getlist('photos')
        print(multiple_images, 'multiple_images')
        for img in multiple_images:
            image = Image.objects.create(car=car, images=img)
            image.save()

        return redirect(reverse('advertisements:cars'))


class EditCarView(TitleMixin, UserPassesTestMixin, UpdateView):
    model = Car
    form_class = CarEditForm
    template_name = 'edit_post.html'
    title = "CarSell - Редактирование объявления"

    def test_func(self):
        return self.request.user == self.get_object().username

    def get_success_url(self):
        user_profile_url = reverse('users:profile', kwargs={'pk': self.request.user.id})

        return user_profile_url

    def form_valid(self, form):
        response = super().form_valid(form)

        print('form form form')
        print(self.request.FILES, 'files')
        print(self.model.pk)
        for f in self.request.FILES.getlist('photos'):
            print(f)
            data = f.read()
            image = Image.objects.create(car=self.object, images=f)
            image.save()
        return redirect(reverse('advertisements:cars'))
        # return response


class DeleteCarView(UserPassesTestMixin, View):

    def test_func(self):
        car = get_object_or_404(Car, pk=self.kwargs['pk'])
        return self.request.user == car.username

    def get(self, request, pk):
        car = get_object_or_404(Car, pk=pk)

        car.delete()

        return HttpResponseRedirect(reverse('users:profile', kwargs={'pk': request.user.id}))


class UserProfileEditView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'edit_profile.html'

    def test_func(self):
        return self.request.user.id == self.kwargs.get('pk')

    def get(self, request, *args, **kwargs):
        print(self.kwargs.get('pk'), self.request.user.id)
        form = UserProfileEditForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse('users:profile', kwargs={'pk': request.user.id}))

        return render(request, self.template_name, {'form': form})


def delete_photo(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    car_id = image.car.id
    image.delete()
    return redirect('users:edit_car', pk=car_id)
