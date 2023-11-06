from datetime import datetime

from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth

from advertisements.models import Car, Image
from users.forms import UserRegistrationForm, UserLoginForm, UserProfileForm, PostCreationForm, ImageCreationForm
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
    context = {
        'form': form
    }

    return render(request, 'create_post.html', context)
