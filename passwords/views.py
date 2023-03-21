from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.hashers import check_password

from passwords.forms import AddPasswordForm, DeletePasswordForm
from passwords.models import UserPassword, Profile

class AddPasswordView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = AddPasswordForm(request.POST, user=request.user)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
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

class PasswordView(LoginRequiredMixin, View):
    def post(self, request, pass_id, *args, **kwargs):
        form_master = request.POST['master_password']
        correct_master = Profile.objects.get(user=request.user).master_password
        if check_password(form_master, correct_master):
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
                'master_check': False
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
            }
        )

class DeletePasswordView(LoginRequiredMixin, View):
    def post(self, request, pass_id, *args, **kwargs):
        form = DeletePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            deleted, rows = UserPassword.objects.filter(id=pass_id).delete()
            if deleted:
                message = "The password has been deleted."
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