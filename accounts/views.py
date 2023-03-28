from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect

from passwords.utils import get_client_ip
from .forms import UserRegistrationForm, ChangeMasterPasswordForm, DeleteUserForm
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views import View
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import ActionLog


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
            login(request, user)
            return redirect('dashboard')
        return render(request, 'registration/register.html', {'form': form, 'title': 'Sign up'})


class ProfileView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = ChangeMasterPasswordForm(request.POST, profile=request.user.profile, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'The master password has been updated.')

            ActionLog.objects.create(
                profile=request.user.profile,
                action='The master password has been changed',
                ip_address=get_client_ip(request),
                danger_level=1
            )

            return redirect('profile')

        return render(
            request,
            'accounts/profile.html',
            {
                'title': 'Profile',
                'active': 'profile',
                'form': form
            }
        )

    def get(self, request, *args, **kwargs):
        return render(
            request,
            'accounts/profile.html',
            {
                'title': 'Profile',
                'active': 'profile',
                'form': ChangeMasterPasswordForm(profile=request.user.profile, instance=request.user.profile)
            }
        )


class DeleteProfileView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = DeleteUserForm(request.POST, profile=request.user.profile)
        if form.is_valid():
            deleted, rows = request.user.delete()
            if deleted:
                message = "The profile has been deleted."
            else:
                message = "The profile hasn't been deleted."
            messages.success(request, message)
            return redirect('login')

        return render(
            request,
            'accounts/delete_profile.html',
            {
                'title': 'Delete account',
                'active': 'profile',
                'form': form
            }
        )

    def get(self, request, *args, **kwargs):
        return render(
            request,
            'accounts/delete_profile.html',
            {
                'title': 'Delete account',
                'active': 'profile',
                'form': DeleteUserForm(profile=request.user.profile)
            }
        )


class ActionLogView(LoginRequiredMixin, ListView):
    model = ActionLog
    paginate_by = 100
    template_name = 'accounts/action_logs.html'
    context_object_name = 'action_logs'
    extra_context = {'title': 'Action logs', 'active': 'action logs', 'n': range(100)}

    def get_queryset(self):
        return ActionLog.objects.filter(profile=self.request.user.profile).order_by('-execution_at')

    # def get(self, request, *args, **kwargs):
    #     return render(
    #         request,
    #         'accounts/action_logs.html',
    #         {
    #             'title': 'Action logs',
    #             'active': 'action logs',
    #             'action_logs': ActionLog.objects.filter(profile=request.user.profile)
    #         }
    #     )
