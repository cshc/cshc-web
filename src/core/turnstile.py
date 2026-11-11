"""
Cloudflare Turnstile form field and widget.

Ref: https://developers.cloudflare.com/turnstile/

Deliberately self-contained (stdlib only) so it works with our Django version.
Requires settings.TURNSTILE_SITE_KEY and settings.TURNSTILE_SECRET_KEY.
"""
import json
import logging
import socket
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from django import forms
from django.conf import settings
from django.utils.html import format_html

LOG = logging.getLogger(__name__)

JS_API_URL = 'https://challenges.cloudflare.com/turnstile/v0/api.js'
VERIFY_URL = 'https://challenges.cloudflare.com/turnstile/v0/siteverify'
VERIFY_TIMEOUT = 5  # seconds

# Name of the POST parameter the Turnstile JS adds to the enclosing form
RESPONSE_PARAM = 'cf-turnstile-response'


def get_client_ip(request):
    """ Best-effort client IP. Prod sits behind a load balancer, so prefer the
        first X-Forwarded-For entry. Only used as a hint to Turnstile.
    """
    if request is None:
        return None
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


class TurnstileWidget(forms.Widget):
    """ Renders the Turnstile script and placeholder div.

        theme: 'light', 'dark' or 'auto'. Turnstile's own default is 'auto'
        (follows the visitor's OS setting), but the site itself has no dark
        mode, so default to 'light'.
    """

    def __init__(self, attrs=None, theme='light'):
        super().__init__(attrs)
        self.theme = theme

    def value_from_datadict(self, data, files, name):
        return data.get(RESPONSE_PARAM)

    def render(self, name, value, attrs=None, renderer=None):
        return format_html(
            '<script src="{}" async defer></script>'
            '<div class="cf-turnstile" data-sitekey="{}" data-theme="{}"></div>',
            JS_API_URL, settings.TURNSTILE_SITE_KEY, self.theme)


class TurnstileField(forms.Field):
    """ Form field that verifies a Turnstile token server-side.

        After validation, self.last_result holds the siteverify response
        (or a synthetic one describing a local failure), for diagnostics.
    """
    widget = TurnstileWidget
    default_error_messages = {
        'required': 'Please complete the verification check.',
        'invalid': 'Please complete the verification check.',
        'unavailable': 'The verification check could not be completed. Please try again.',
    }

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', '')
        super().__init__(*args, **kwargs)
        self.remote_ip = None
        self.last_result = None

    def validate(self, value):
        self.last_result = None
        super().validate(value)   # 'required' check
        result = self.verify(value)
        self.last_result = result
        if result.get('unavailable'):
            raise forms.ValidationError(self.error_messages['unavailable'], code='unavailable')
        if not result.get('success'):
            raise forms.ValidationError(self.error_messages['invalid'], code='invalid')

    def verify(self, token):
        """ Call siteverify. Never raises; returns a dict. """
        params = {'secret': settings.TURNSTILE_SECRET_KEY, 'response': token}
        if self.remote_ip:
            params['remoteip'] = self.remote_ip
        request = Request(VERIFY_URL, urlencode(params).encode('utf-8'))
        try:
            with urlopen(request, timeout=VERIFY_TIMEOUT) as response:
                return json.loads(response.read().decode('utf-8'))
        except (URLError, socket.timeout, OSError, ValueError) as ex:
            # URLError covers HTTPError; ValueError covers bad JSON
            LOG.warning("Turnstile verification failed: %s", ex)
            return {'success': False, 'unavailable': True, 'error-codes': ['local:' + type(ex).__name__]}
