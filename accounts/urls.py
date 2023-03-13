from django.contrib import admin
from django.contrib.auth import views
from django.urls import path, include

urlpatterns =[
    path('login/', views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', views.LogoutView.as_view(), {'next': '/successfully_logged_out/'},name='logout'),
    path('register/', ),
]