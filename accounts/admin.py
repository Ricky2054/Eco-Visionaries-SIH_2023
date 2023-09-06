from django.contrib import admin

from accounts.models import User

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('phone', 'email', 'first_name', 'last_login', 'is_staff')
    fieldsets = [
        ("User Details", {
            "fields": (
                ['phone', 'email', 'password', 'first_name', 'last_name']
            ),
        }),
        ("More Details", {
            "fields": (
                ['date_joined', 'last_login', 'last_logout']
            ), 'classes': ['collapse']
        }),
        ("Permissions", {
            "fields": (
                ['is_staff', 'is_superuser', 'is_active', 'user_permissions', 'groups']
            ), 'classes': ['collapse']
        }),
    ]

