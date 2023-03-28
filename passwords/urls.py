from django.contrib.auth import views as django_auth_views
from django.urls import path, include
from django.views.generic.base import RedirectView

from passwords.views import *

urlpatterns =[
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('', RedirectView.as_view(url='dashboard/')),
    path('add/password/', AddPasswordView.as_view(), name='add_password'),
    path('password/<int:pass_id>', PasswordView.as_view(), name='view_password'),
    path('password/delete/<int:pass_id>', DeletePasswordView.as_view(), name='delete_password'),
]
