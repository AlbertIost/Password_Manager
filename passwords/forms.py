from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError

from .models import UserPassword

class AddPasswordForm(forms.ModelForm):
    website_name = forms.CharField(label='Website name')
    website_link = forms.URLField(label='Website link')
    website_username = forms.CharField(label='Website username')
    website_password = forms.CharField(label='Website password')
    website_notes = forms.CharField(label='Website notes')
    master_password = forms.CharField(widget=forms.PasswordInput(), label='Master password')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(AddPasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        form_master = self.cleaned_data.get('master_password')
        hashed_master = self.user.profile.master_password
        if check_password(form_master, hashed_master):
            return super().clean()

        self.add_error('master_password', '')
        raise ValidationError('Enter the correct master password.')


    class Meta:
        model = UserPassword
        fields = ['website_name', 'website_link', 'website_username', 'website_password', 'website_notes', 'master_password']

class DeletePasswordForm(forms.ModelForm):
    master_password = forms.CharField(widget=forms.PasswordInput(), label='Master password')
    def clean(self):
        correct_master = self.user.profile.master_password
        if not check_password(self.cleaned_data['master_password'], correct_master):
            raise ValidationError('Invalid master password.')
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(DeletePasswordForm, self).__init__(*args, **kwargs)
    class Meta:
        model = UserPassword
        fields = ['master_password']

class PasswordViewForm(forms.Form):
    master_password = forms.CharField(widget=forms.PasswordInput(), label='')
    def clean(self):
        correct_master = self.profile.master_password
        if not check_password(self.cleaned_data['master_password'], correct_master):
            raise ValidationError('Invalid master password.')

    def __init__(self, *args, **kwargs):
        self.profile = kwargs.pop('profile', None)
        super(PasswordViewForm, self).__init__(*args, **kwargs)