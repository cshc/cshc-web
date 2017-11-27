"""
Forms for general CSHC app use
"""
from django import forms
from django.contrib.flatpages.models import FlatPage
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from zinnia.models import Entry, Category
from zinnia.admin.forms import EntryAdminForm, CategoryAdminForm
from .models import JuniorsContactSubmission, ContactSubmission


class SignupForm(forms.Form):
    """ Custom form for additional sign-up information """
    first_name = forms.CharField(max_length=30, label='First name')
    last_name = forms.CharField(max_length=30, label='Last name')

    def signup(self, request, user):
        """ 
        Required method that is called by the django-allauth's form when saving
        a new user.
        """
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()


class ContactSubmissionForm(forms.ModelForm):
    """ Form used for the contact form"""

    class Meta:
        """ Meta-info for the form. """
        model = ContactSubmission
        # our_notes is only to be used by staff/admin
        exclude = ('our_notes',)


class JuniorsContactSubmissionForm(forms.ModelForm):
    """ Form used for the contact form"""

    class Meta:
        """ Meta-info for the form. """
        model = JuniorsContactSubmission
        # our_notes is only to be used by staff/admin
        exclude = ('our_notes',)


class FlatPageAdminForm(forms.ModelForm):
    """ Form for editing matches in the admin interface """
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = FlatPage
        exclude = []


class ZinniaEntryAdminForm(EntryAdminForm):
    """ Overrides the default admin form, adding a couple of redactor
        editor widget.
    """
    content = forms.CharField(widget=CKEditorUploadingWidget())
    excerpt = forms.CharField(widget=CKEditorUploadingWidget())
    lead = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        """ Meta-info for the form. """
        model = Entry
        exclude = []


class ZinniaCategoryAdminForm(CategoryAdminForm):
    """ Overrides the default admin form, adding a redactor editor widget. """
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        """ Meta-info for the form. """
        model = Category
        exclude = []
