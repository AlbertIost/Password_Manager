from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.hashers import check_password

from accounts.models import ActionLog
from passwords.forms import AddPasswordForm, DeletePasswordForm, PasswordViewForm
from passwords.models import UserPassword, Profile
from passwords.utils import get_client_ip


class AddPasswordView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = AddPasswordForm(request.POST, user=request.user)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            ActionLog.objects.create(
                profile=request.user.profile,
                action='Add password.',
                note=f'Password for {form.instance.website_link}',
                ip_address=get_client_ip(request),

            )

            return redirect('dashboard')

        return render(
            request,
            'passwords/add_new.html',
            {
                'title': 'Add new password',
                'form': form,
                'active': 'add password'
            }
        )

    def get(self, request, *args, **kwargs):
        return render(
            request,
            'passwords/add_new.html',
            {
                'title': 'Add new password',
                'form': AddPasswordForm(user=request.user),
                'active': 'add password'
            }
        )


class DashboardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        passwords = UserPassword.objects.filter(user=request.user)
        return render(
            request,
            'passwords/dashboard.html',
            {
                'title': 'Dashboard',
                'active': 'dashboard',
                'passwords': passwords
            }
        )


class PasswordView(UserPassesTestMixin, LoginRequiredMixin, View):
    def test_func(self):
        pass_id = self.kwargs['pass_id']
        return UserPassword.objects.get(id=pass_id).user == self.request.user

    def post(self, request, pass_id, *args, **kwargs):
        form = PasswordViewForm(request.POST, profile=request.user.profile)
        if form.is_valid():
            ActionLog.objects.create(
                profile=request.user.profile,
                action='The password was viewed using the master password.',
                note=f'password_id:{pass_id}',
                ip_address=get_client_ip(request)
            )
            return render(
                request,
                'passwords/password.html',
                {
                    'title': 'Password',
                    'active': 'dashboard',
                    'password': UserPassword.objects.get(id=pass_id),
                    'master_check': True
                }
            )

        return render(
            request,
            'passwords/password.html',
            {
                'title': 'Password',
                'active': 'dashboard',
                'password': UserPassword.objects.get(id=pass_id),
                'form': form,
            }
        )

    def get(self, request, pass_id, *args, **kwargs):
        return render(
            request,
            'passwords/password.html',
            {
                'title': 'Password',
                'active': 'dashboard',
                'password': UserPassword.objects.get(id=pass_id),
                'form': PasswordViewForm(profile=request.user.profile)
            }
        )


class DeletePasswordView(UserPassesTestMixin, LoginRequiredMixin, View):
    def test_func(self):
        pass_id = self.kwargs['pass_id']
        return UserPassword.objects.get(id=pass_id).user == self.request.user

    def post(self, request, pass_id, *args, **kwargs):
        form = DeletePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            website_link = UserPassword.objects.filter(id=pass_id).get().website_link
            deleted, rows = UserPassword.objects.filter(id=pass_id).delete()
            if deleted:
                message = "The password has been deleted."
                ActionLog.objects.create(
                    profile=request.user.profile,
                    action='The password has been deleted.',
                    note=f'Password for {website_link}',
                    ip_address=get_client_ip(request)
                )
            else:
                message = "The password hasn't been deleted."
            messages.success(request, message)
            return redirect('dashboard')

        return render(
            request,
            'accounts/delete_profile.html',
            {
                'title': 'Delete password',
                'active': 'profile',
                'form': form
            }
        )

    def get(self, request, *args, pass_id, **kwargs):
        return render(
            request,
            'accounts/delete_profile.html',
            {
                'title': 'Delete password',
                'active': 'profile',
                'form': DeletePasswordForm(user=request.user)
            }
        )
