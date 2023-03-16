from django.contrib.auth import views as django_auth_views
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from passwords import views as passwords_views

path('dashboard/', login_required(passwords_views.DashboardView.as_view()), name='dashboard')