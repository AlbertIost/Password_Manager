from django.contrib import admin

from accounts.models import ActionLog


# Register your models here.
@admin.register(ActionLog)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('profile', 'action', 'note', 'ip_address', 'danger_level', 'execution_at')
    readonly_fields = ['ip_address']
    fields = ('profile', 'action', 'note', 'ip_address', 'danger_level', 'execution_at')