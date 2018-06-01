""" Custom forms for the Member models.
"""

from django import forms
from geoposition.widgets import GeopositionWidget
from allauth.account.forms import SignupForm, LoginForm, AddEmailForm, ChangePasswordForm, SetPasswordForm, ResetPasswordForm, ResetPasswordKeyForm
from unify.widgets import UnifyTextInput, UnifyTextarea, UnifySelect, UnifyDateInput, UnifyPhoneInput
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
            'first_name': UnifyTextInput(left_icon='fas fa-user'),
            'known_as': UnifyTextInput(left_icon='fas fa-user'),
            'last_name': UnifyTextInput(left_icon='fas fa-user'),
            'profile_pic': CshcCropWidget,
            'pref_position': UnifySelect,
            'phone': UnifyPhoneInput,
            'addr_street': UnifyTextInput(attrs={'placeholder': 'Street'}),
            'addr_line2': UnifyTextInput(),
            'addr_town': UnifyTextInput(attrs={'placeholder': 'Town/city'}),
            'addr_postcode': UnifyTextInput(attrs={'placeholder': 'Post code'}),
            'addr_position': GeopositionWidget,
            'dob': UnifyDateInput,
            'emergency_contact': UnifyTextInput(),
            'emergency_relationship': UnifySelect,
            'emergency_phone': UnifyPhoneInput,
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


class UnifyLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].widget = UnifyTextInput(
            attrs={
                'placeholder': 'E-mail address',
                'class': 'g-py-15 g-pr-15',
            },
            left_icon='fas fa-envelope')

        self.fields['password'].widget = UnifyTextInput(
            attrs={
                'placeholder': 'Password',
                'class': 'g-py-15 g-pr-15',
            },
            left_icon='fas fa-lock')


class UnifySignupForm(SignupForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = UnifyTextInput(
            attrs={
                'placeholder': 'Password',
                'class': 'g-py-15 g-pr-15',
            },
            left_icon='fas fa-lock')

        self.fields['password2'].widget = UnifyTextInput(
            attrs={
                'placeholder': 'Retype password',
                'class': 'g-py-15 g-pr-15',
            },
            left_icon='fas fa-lock')


class UnifyAddEmailForm(AddEmailForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget = UnifyTextInput(attrs={'placeholder': 'E-mail address'},
                                                     left_icon='fas fa-envelope')


class UnifyResetPasswordForm(ResetPasswordForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget = UnifyTextInput(attrs={'placeholder': 'E-mail address'},
                                                     left_icon='fas fa-envelope')


class UnifyResetPasswordKeyForm(ResetPasswordKeyForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = UnifyTextInput(attrs={'placeholder': 'New Password'},
                                                         left_icon='fas fa-lock')
        self.fields['password2'].widget = UnifyTextInput(attrs={'placeholder': 'New Password (again)'},
                                                         left_icon='fas fa-lock')


class UnifySetPasswordForm(SetPasswordForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = UnifyTextInput(attrs={'placeholder': 'New Password'},
                                                         left_icon='fas fa-lock')
        self.fields['password2'].widget = UnifyTextInput(attrs={'placeholder': 'New Password (again)'},
                                                         left_icon='fas fa-lock')


class UnifyChangePasswordForm(ChangePasswordForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['oldpassword'].widget = UnifyTextInput(attrs={'placeholder': 'Current Password'},
                                                           left_icon='fas fa-lock')
        self.fields['password1'].widget = UnifyTextInput(attrs={'placeholder': 'New Password'},
                                                         left_icon='fas fa-lock')
        self.fields['password2'].widget = UnifyTextInput(attrs={'placeholder': 'New Password (again)'},
                                                         left_icon='fas fa-lock')
