from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UserRegistrationForm
from django.views import View
from django.conf import settings
# Create your views here.

class RegisterView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

        return render(request, 'registration/register.html', {'form': UserRegistrationForm(), 'title': 'Sign up'})

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('dashboard')
        return render(request, 'registration/register.html', {'form': form, 'title': 'Sign up'})

class DashboardView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'passwords/dashboard.html', {'title': 'Dashboard'})