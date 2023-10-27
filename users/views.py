from datetime import datetime

from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth

from advertisements.models import Car
from users.forms import UserRegistrationForm, UserLoginForm, UserProfileForm, PostCreationForm
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


def profile(request):
    form = UserProfileForm(instance=request.user)
    print(request.user)
    advertisements = Car.objects.filter(username=request.user)
    print(advertisements)

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
            print(post.price)
            # print(post.username)
            post.save()
            return redirect(reverse('advertisements:cars'))

        else:
            print(form.errors)

    form = []
    context = {
        'form': form
    }

    return render(request, 'create_post.html', context)
