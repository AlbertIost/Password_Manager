from django.contrib.auth import views as django_auth_views
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.views.generic.base import RedirectView

from passwords import views as passwords_views

urlpatterns =[
    path('dashboard/', login_required(passwords_views.DashboardView.as_view()), name='dashboard'),
    path('', RedirectView.as_view(url='dashboard/'))
]
