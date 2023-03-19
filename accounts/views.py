from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UserRegistrationForm
from django.views.generic.edit import CreateView
from django.views import View
from django.conf import settings

# Create your views here.

class RegisterView(CreateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

        return render(request, 'registration/register.html', {
            'form': UserRegistrationForm(),
            'title': 'Sign up'
        })

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()

            # Hashing user master password
            user.profile.master_password = form.cleaned_data.get('master_password')

            user.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('dashboard')
        return render(request, 'registration/register.html', {'form': form, 'title': 'Sign up'})


class ProfileView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            'accounts/profile.html',
            {
                'title': 'Profile',
                'active': 'profile'
            }
        )