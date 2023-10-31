"""
Django admin modifications
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _ #gettext_lazy is a helper function from django to convert strings to human readable text

from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for Users"""
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}), #None is the title of the section
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser'
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ('last_login',) #we can't edit the last_login field
    add_fieldsets = (
        (None, {
            'classes': ('wide',), #classes is a css class that we can apply to the form (wide is a class that makes the form full width)
            'fields': ('email', 'password1', 'password2', 'name', 'is_active', 'is_staff', 'is_superuser') #password1 and password2 are the default fields for password
        }),
    )

admin.site.register(models.User, UserAdmin)
admin.site.register(models.Recipe)