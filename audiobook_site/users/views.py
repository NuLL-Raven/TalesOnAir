from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, EmailOrUsernameAuthenticationForm

from django.contrib.auth import login
from .models import User, Subscription


def sign_up(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            subscription = Subscription.objects.get(type='FREE')
            user.subscription = subscription
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/sign_up.html', {'form': form})



def sign_in(request):
    if request.method == 'POST':
        form = EmailOrUsernameAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = EmailOrUsernameAuthenticationForm()
    return render(request, 'users/sign_in.html', {'form': form})
