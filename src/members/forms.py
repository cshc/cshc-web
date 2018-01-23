""" Custom forms for the Member models.
"""

from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from geoposition.widgets import GeopositionWidget
from unify.widgets import UnifyTextInput, UnifyTextarea, UnifySelect, UnifyDateInput
from core.widgets import CshcCropWidget
from .models import Member


class MemberProfileForm(forms.ModelForm):
    """Form used to edit your own profile"""

    def __init__(self, *args, **kwargs):
        super(MemberProfileForm, self).__init__(*args, **kwargs)
        self.fields['dob'].input_formats = ['%d-%m-%Y']

    class Meta:
        """ Meta-info for the form."""
        model = Member
        widgets = {
            'first_name': UnifyTextInput(left_icon='icon-user-follow'),
            'known_as': UnifyTextInput(left_icon='icon-user-follow'),
            'last_name': UnifyTextInput(left_icon='icon-user-follow'),
            'profile_pic': CshcCropWidget,
            'pref_position': UnifySelect,
            'shirt_number': UnifyTextInput(attrs={'class': 'g-width-100 flex-0'}),
            'phone': UnifyTextInput(left_icon='fa fa-phone'),
            'addr_street': UnifyTextInput(attrs={'placeholder': 'Street'}),
            'addr_line2': UnifyTextInput(),
            'addr_town': UnifyTextInput(attrs={'placeholder': 'Town/city'}),
            'addr_postcode': UnifyTextInput(attrs={'placeholder': 'Post code'}),
            'addr_position': GeopositionWidget,
            'dob': UnifyDateInput,
            'emergency_contact': UnifyTextInput(),
            'emergency_relationship': UnifySelect,
            'emergency_phone': UnifyTextInput(left_icon='fa fa-phone'),
            'medical_notes': UnifyTextarea(attrs={'rows': '5'}),
            'email': forms.HiddenInput(),
        }
        labels = {
            'addr_street': 'Address',
        }
        help_texts = {
            'emergency_relationship': 'Your emergency contact\'s relationship to you',
            'shirt_number': 'Only set this if you have actually been assigned a shirt number',
        }
        fields = ('email', 'first_name', 'known_as', 'last_name', 'profile_pic', 'profile_pic_cropping',                             # Personal
                  # Playing
                  'pref_position', 'shirt_number',
                  # Contact
                  'phone', 'addr_street', 'addr_line2', 'addr_town', 'addr_postcode', 'addr_position',
                  'dob', 'emergency_contact', 'emergency_relationship', 'emergency_phone', 'medical_notes',     # Medical
                  )
