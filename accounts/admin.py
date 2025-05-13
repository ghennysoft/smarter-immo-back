from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from  django.contrib.auth import get_user_model


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'phone', 'password')}),
        (('Personnal Info'), {'fields': ('first_name', 'last_name')}),
        (('Permissions'), {'fields': ('is_superuser', 'is_staff', 'is_active', 'groups', 'user_permissions')}),
        (('Importants dates'), {'fields': ('last_login', 'date_joined')}),
    )

    """For new User"""
    add_fieldsets =(
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'password'),
        }),
    ) 
    list_display = ('email', 'first_name', 'last_name', 'phone', 'is_staff')
    search_fields = ('email', 'phone', 'first_name', 'last_name')
    ordering = ('email',)


admin.site.register(get_user_model(), CustomUserAdmin)
