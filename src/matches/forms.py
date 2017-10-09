"""
Forms for the Matches app
"""
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Match


class MatchAdminForm(forms.ModelForm):
    """ Form for editing matches in the admin interface """
    report_body = forms.CharField(widget=CKEditorUploadingWidget())
    pre_match_hype = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Match
        exclude = []
