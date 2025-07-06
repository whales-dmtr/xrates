from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout


def login_view(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            login(request, login_form.get_user())
            return redirect('rates')
    else:
        login_form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': login_form})


def register_view(request):
    if request.method == 'POST':
        register_form = UserCreationForm(request.POST)
        if register_form.is_valid():
            login(request, register_form.save())
            return redirect('rates')
    else:
        register_form = UserCreationForm()

    return render(request, 'users/register.html', {'form': register_form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('rates')