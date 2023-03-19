from django.contrib.auth import views as django_auth_views
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.views.generic.base import RedirectView

from passwords.views import *

urlpatterns =[
    path('dashboard/', login_required(DashboardView.as_view()), name='dashboard'),
    path('', RedirectView.as_view(url='dashboard/')),
    path('add/password/', AddPasswordView.as_view(), name='add_password'),
    path('password/<int:pass_id>', PasswordView.as_view(), name='view_password')
]
