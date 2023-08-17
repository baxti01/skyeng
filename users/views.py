from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from users.forms import LoginForm, UserCreationForm


def sign_up(request):
    form = UserCreationForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('users:login')

    return render(request, 'users/sign_up.html', {'form': form})


def login_view(request):
    form = LoginForm(request.POST or None)

    if form.is_valid():
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email, password=password)
        login(request, user)

        return redirect('home')

    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')
