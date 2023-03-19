from django.contrib import admin

from passwords.models import Profile, UserPassword


# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar_tag', 'master_password')
    readonly_fields = ['avatar_tag']
    fields = ('user', 'avatar_tag', 'master_password')


@admin.register(UserPassword)
class UserPasswordAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'website_name',
        'website_link',
        'website_username',
        'website_password',
        'website_notes'
    )
    fields = (
        'user',
        'website_name',
        'website_link',
        'website_username',
        'website_password',
        'website_notes'
    )