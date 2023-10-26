from django.shortcuts import render, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import auth

from users.forms import UserRegistrationForm, UserLoginForm, UserProfileForm
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
    context = {
        'form': form,
    }

    return render(request, 'profile.html', context=context)
