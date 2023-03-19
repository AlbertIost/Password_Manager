from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password

from passwords.models import Profile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    master_password = forms.CharField(
        label='Master password',
        help_text='The master password will be used to encrypt ad decrypt your password.'
    )


    def clean_master_password(self):
        return make_password(self.cleaned_data.get('master_password'))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'master_password']