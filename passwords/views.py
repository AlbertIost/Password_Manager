from django.shortcuts import render, redirect
from django.views import View
from passwords.forms import AddPasswordForm

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
        return render(
            request,
            'passwords/dashboard.html',
            {
                'title': 'Dashboard',
                'active': 'dashboard'
            }
        )