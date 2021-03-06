from django.shortcuts import render

from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse
from users.forms import CustomUserCreationForm


def index(request):
    return render(request, "index.html")


def register(request):
    if request.method == "GET":
        return render(
            request, "users/register.html",
            {"form": CustomUserCreationForm}
        )
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('investimentos:index'))
        else:
            return render(request, 'users/register.html', {'errors': form.errors, 'form': CustomUserCreationForm})
