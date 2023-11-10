from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth
from django.views import View

from advertisements.models import Car, Image, CarBrand, CarModel, CarGeneration
from users.forms import UserRegistrationForm, UserLoginForm, UserProfileForm, PostCreationForm, ImageCreationForm, \
    CarForm
from users.models import User


def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            print(username, password)
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return HttpResponseRedirect(reverse('advertisements:cars'))

    else:
        form = UserLoginForm()

    context = {'form': form}

    return render(request, "login.html", context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('advertisements:cars'))


def registration(request):
    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('advertisements:cars'))

    else:
        form = UserRegistrationForm()

    context = {'form': form}

    return render(request, "registration.html", context)


def profile(request, pk):
    if not pk:
        form = UserProfileForm(instance=request.user)
        advertisements = Car.objects.filter(username=request.user)
    else:
        form = UserProfileForm(instance=User.objects.get(pk=pk))
        advertisements = Car.objects.filter(username=User.objects.get(pk=pk))
    context = {
        'form': form,
        'advertisements': advertisements
    }

    return render(request, 'profile.html', context=context)


def create_post(request):
    if request.method == "POST":
        print(request.POST)
        form = PostCreationForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.username = request.user
            post.created_timestamp = datetime.now()
            post.save()

        else:
            print(form.errors)

        for f in request.FILES.getlist('photos'):
            last_post = Car.objects.filter(username=request.user).last()
            data = f.read()
            image = Image.objects.create(car=last_post, images=f)
        return redirect(reverse('advertisements:cars'))
        # if image.is_valid():
        #     image.save()
        #     print(image.errors)

        # imageform = ImageCreationForm()

    form = []
    form = CarForm()
    context = {
        'form': form
    }

    return render(request, 'create_post.html', context)


class GetModels(View):
    def get(self, request):
        # print(request.GET)
        brand_id = request.GET.get('brand_id')
        # print(brand_id)
        if brand_id is not None:
            models = CarModel.objects.filter(brand=brand_id)
            # print(models, 'models')
            model_data = [{'id': model.id, 'name': model.get_model()} for model in models]
            # print(model_data)
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
