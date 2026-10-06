"""
Allauth adapters for the CSHC Website.
"""
from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.providers.base import AuthProcess
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

from core.models import CshcUser


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Custom social account adapter.

    If a user tries to sign in with a social account (e.g. Google) whose email
    address already belongs to an existing CSHC account that has not linked that
    social provider, redirect them back to the sign-in page with a message
    explaining what to do.
    """

    def pre_social_login(self, request, sociallogin):
        if sociallogin.is_existing:
            return

        if sociallogin.state.get('process') == AuthProcess.CONNECT:
            return

        email = (sociallogin.user.email or '').strip().lower()
        if not email:
            return

        if not CshcUser.objects.filter(email__iexact=email).exists():
            return

        provider_name = sociallogin.account.get_provider().name
        messages.error(
            request,
            "The {provider} account {email} isn't linked to a Cambridge South "
            "account. Please sign in with your email address and password, then "
            "link your {provider} account from your member profile.".format(
                provider=provider_name,
                email=email,
            ),
        )
        raise ImmediateHttpResponse(redirect(reverse('account_login')))
