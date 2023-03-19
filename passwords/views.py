from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.hashers import check_password

from passwords.forms import AddPasswordForm
from passwords.models import UserPassword, Profile

class AddPasswordView(View):
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

class DashboardView(View):
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

class PasswordView(View):
    def post(self, request, pass_id, *args, **kwargs):
        form_master = request.POST['master_password']
        correct_master = Profile.objects.get(user=request.user).master_password
        print(check_password(form_master, correct_master))
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