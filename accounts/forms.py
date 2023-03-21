from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError

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


class ChangeMasterPasswordForm(forms.ModelForm):
    current_master_password = forms.CharField(widget=forms.PasswordInput(), label='Master password')
    master_password = forms.CharField(widget=forms.PasswordInput(), label='New master password')
    master_password2 = forms.CharField(widget=forms.PasswordInput(), label='Confirm master password')

    def __init__(self, *args, **kwargs):
        self.profile = kwargs.pop('profile', None)
        super(ChangeMasterPasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        correct_master = self.profile.master_password
        if not check_password(self.cleaned_data['current_master_password'], correct_master):
            raise ValidationError('Invalid master password.')

        if not check_password(self.cleaned_data['master_password2'], self.cleaned_data['master_password']):
            raise ValidationError('Passwords don\'t match.')

    def clean_master_password(self):
        return make_password(self.cleaned_data['master_password'])

    class Meta:
        model = Profile
        fields = ['current_master_password', 'master_password', 'master_password2']


class DeleteUserForm(forms.Form):
    master_password = forms.CharField(widget=forms.PasswordInput(), label='Master password')
    def clean(self):
        correct_master = self.profile.master_password
        if not check_password(self.cleaned_data['master_password'], correct_master):
            raise ValidationError('Invalid master password.')
    def __init__(self, *args, **kwargs):
        self.profile = kwargs.pop('profile', None)
        super(DeleteUserForm, self).__init__(*args, **kwargs)
