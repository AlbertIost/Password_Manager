from django.contrib import admin

from passwords.models import Profile


# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar_tag', 'secret_key')
    readonly_fields = ['avatar_tag']
    fields = ('user', 'avatar_tag', 'secret_key')