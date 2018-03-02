""" Custom forms for the Member models.
"""

from django import forms
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
            'first_name': UnifyTextInput(left_icon='icon-user'),
            'known_as': UnifyTextInput(left_icon='icon-user'),
            'last_name': UnifyTextInput(left_icon='icon-user'),
            'profile_pic': CshcCropWidget,
            'pref_position': UnifySelect,
            'phone': UnifyTextInput(left_icon='fas fa-phone'),
            'addr_street': UnifyTextInput(attrs={'placeholder': 'Street'}),
            'addr_line2': UnifyTextInput(),
            'addr_town': UnifyTextInput(attrs={'placeholder': 'Town/city'}),
            'addr_postcode': UnifyTextInput(attrs={'placeholder': 'Post code'}),
            'addr_position': GeopositionWidget,
            'dob': UnifyDateInput,
            'emergency_contact': UnifyTextInput(),
            'emergency_relationship': UnifySelect,
            'emergency_phone': UnifyTextInput(left_icon='fas fa-phone'),
            'medical_notes': UnifyTextarea(attrs={'rows': '5'}),
            'email': forms.HiddenInput(),
        }
        labels = {
            'addr_street': 'Address',
        }
        help_texts = {
            'emergency_relationship': 'Your emergency contact\'s relationship to you',
        }
        fields = ('email', 'first_name', 'known_as', 'last_name', 'profile_pic', 'profile_pic_cropping',                             # Personal
                  # Playing
                  'pref_position',
                  # Contact
                  'phone', 'addr_street', 'addr_line2', 'addr_town', 'addr_postcode', 'addr_position',
                  'dob', 'emergency_contact', 'emergency_relationship', 'emergency_phone', 'medical_notes',     # Medical
                  )
