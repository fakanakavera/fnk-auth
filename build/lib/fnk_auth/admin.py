from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserAccountDetails


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active', 'email_verified')
    list_filter = ('is_staff', 'is_active', 'email_verified')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Additional Info', {'fields': ('email_verified',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


class UserAccountDetailsAdmin(admin.ModelAdmin):
    model = UserAccountDetails
    list_display = ['user', 'nick_name']
    list_filter = ['user', 'nick_name']
    search_fields = ('user', 'nick_name')
    ordering = ('user',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserAccountDetails, UserAccountDetailsAdmin)
