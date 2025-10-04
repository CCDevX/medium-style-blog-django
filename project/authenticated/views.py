from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from .forms.loginForm import LoginForm
from .forms.registerForm import RegisterForm
from blog.models import Profile


# Create your views here.

def auth_login(request):
    if request.method == 'POST':
        form = LoginForm(request,request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Vous êtes authentifié.')
                return redirect('blog-home')
            else:
                messages.error(request, 'Le no d\'utilisateur ou le mot de passe est incorrecte.')
    else:
        form = LoginForm()
    return render(request, 'authenticated/login.html', {'form': form})

def auth_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(
                user=user,
                email=user.email
            )
            messages.success(request, 'Votre compte a été crée')
            return redirect('blog-home')
    else:
        form = RegisterForm()
    return render(request, 'authenticated/register.html', {'form': form})

def auth_logout(request):
    logout(request)
    messages.success(request, 'Vous êtes déconnecté.')
    return redirect('blog-home')