
from django.contrib import admin

# Register your models here.


from .models import Shorten


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'url', 'code', 'type', 'counter', 'create_user', 'creater_ip', 'create_at']

# Re-register UserAdmin
admin.site.register(Shorten, UserAdmin)
