"""
Admin configuration for Core Models
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import CshcUser, ClubInfo, JuniorsContactSubmission


@admin.register(CshcUser)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


@admin.register(ClubInfo)
class ClubInfoAdmin(admin.ModelAdmin):
    """ Admin interface definition for the ClubInfo model. """
    list_display = ('key', 'value')


@admin.register(JuniorsContactSubmission)
class JuniorsContactSubmissionAdmin(admin.ModelAdmin):
    """ Admin interface definition for the JuniorsContactSubmission model. """
    ordering = ('child_age', 'child_gender', 'child_name')
    list_filter = ('child_age', 'child_gender')
    search_fields = ('full_name', 'child_name', 'email')
    list_display = ('full_name', 'email', 'child_name',
                    'child_age', 'child_gender', 'submitted')
