from django.contrib.auth import views as django_auth_views
from django.contrib.auth.views import PasswordChangeView
from django.urls import path, include
from django.conf import settings
from accounts import views as accounts_views

urlpatterns =[
    path('login/', django_auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', django_auth_views.LogoutView.as_view(), name='logout'),
    path('register/', accounts_views.RegisterView.as_view(), name='register'),
    path('profile/', accounts_views.ProfileView.as_view(), name='profile'),
    path('delete/', accounts_views.DeleteProfileView.as_view(), name='delete_profile'),
    path('actions/', accounts_views.ActionLogView.as_view(), name='action_logs'),
    path('profile/change/master/', accounts_views.ChangeMasterPasswordView.as_view(), name='change_master'),
    path('profile/change/password/', PasswordChangeView.as_view(success_url=settings.LOGIN_REDIRECT_URL), name='change_password'),
]