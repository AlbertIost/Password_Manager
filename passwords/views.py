from django.shortcuts import render
from django.views import View

from passwords.encryption_util import decrypt
from passwords.models import Profile


# Create your views here.
class DashboardView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            'passwords/dashboard.html',
            {
                'title': 'Dashboard',
                'secret_key': decrypt(Profile.objects.filter(user=request.user).get().secret_key),
            }
        )