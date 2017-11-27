"""
Admin configuration for Core Models
"""

from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _
from zinnia.models import Entry, Category
from zinnia.admin import EntryAdmin, CategoryAdmin

from .models import CshcUser, ClubInfo, JuniorsContactSubmission, ContactSubmission
from .forms import FlatPageAdminForm, ZinniaEntryAdminForm, ZinniaCategoryAdminForm


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


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    """ Admin interface definition for the ContactSubmission model. """
    list_display = ('full_name', 'email', 'submitted')


@admin.register(JuniorsContactSubmission)
class JuniorsContactSubmissionAdmin(admin.ModelAdmin):
    """ Admin interface definition for the JuniorsContactSubmission model. """
    ordering = ('child_age', 'child_gender', 'child_name')
    list_filter = ('child_age', 'child_gender')
    search_fields = ('full_name', 'child_name', 'email')
    list_display = ('full_name', 'email', 'child_name',
                    'child_age', 'child_gender', 'submitted')


admin.site.unregister(FlatPage)


@admin.register(FlatPage)
class CKEditorFlatPageAdmin(FlatPageAdmin):
    """ Override for the FlatPage admin interface - uses a CK Editor widget"""

    form = FlatPageAdminForm
    fieldsets = [
        ('Config', {'fields': ['url', 'title', 'sites', 'content']}),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('enable_comments', 'registration_required', 'template_name')
        }),
    ]


admin.site.unregister(Entry)


@admin.register(Entry)
class ZinniaEntryAdmin(EntryAdmin):
    """ Override the provided admin interface for blog entries - simplify it a bit
        and add support (via a custom form) for WYSIWYG entry.
    """
    form = ZinniaEntryAdminForm

    fieldsets = (
        (_('Content'), {
            'fields': (('title', 'status'), 'lead', 'content', 'featured', 'excerpt')}),
        (_('Illustration'), {
            'fields': ('image', 'image_caption'),
            'classes': ('collapse', 'collapse-closed')}),
        (_('Publication'), {
            'fields': ('publication_date',
                       ('start_publication', 'end_publication'), 'sites'),
            'classes': ('collapse', 'collapse-closed')}),
        # (_('Templates'), {
        #     'fields': ('content_template', 'detail_template'),
        #     'classes': ('collapse', 'collapse-closed')}),
        (_('Metadata'), {
            'fields': ('authors', 'related'),
            'classes': ('collapse', 'collapse-closed')}),
        (None, {'fields': ('comment_enabled', 'categories', 'tags', 'slug')}))


admin.site.unregister(Category)


@admin.register(Category)
class ZinniaCategoryAdmin(CategoryAdmin):
    """ Override the CategoryAdmin interface, specifying our own form. """
    form = ZinniaCategoryAdminForm
