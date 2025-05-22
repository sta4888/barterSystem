from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.views import View

from users.forms import UserRegistrationForm, CustomAuthenticationForm


class RegisterView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, "users/register.html", {"form": form})

    def post(self, request):
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("ads:ad-list")  # замените на нужную страницу
        return render(request, "users/register.html", {"form": form})


class LoginView(View):
    def get(self, request):
        form = CustomAuthenticationForm()
        return render(request, "users/login.html", {"form": form})

    def post(self, request):
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("ads:ad-list")  # замените на нужную страницу
        return render(request, "users/login.html", {"form": form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("users:login")
