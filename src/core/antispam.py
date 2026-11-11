"""
Lightweight, invisible anti-spam checks for public forms.

SpamCheckFormMixin adds:
  - a honeypot field ('website') that real users never see or fill in
  - a signed render timestamp ('form_ts') to catch instant or replayed submissions
  - simple content rules on the 'message' field (the link check is off by default - see BLOCK_URLS)

Any failed checks are recorded in form.spam_reasons during clean() and logged.
By default (ENFORCE = False) that is all that happens: the submission goes
through as normal. With ENFORCE = True the form is refused with a plain,
non-specific error (ENFORCED_ERROR) instead.
"""
import logging
import re
import time

from django import forms
from django.core import signing

LOG = logging.getLogger(__name__)

# Log-only for now: suspected spam is logged but still accepted. Set to True to
# refuse it with ENFORCED_ERROR. The message deliberately doesn't say which check
# failed.
ENFORCE = False
ENFORCED_ERROR = "Sorry, we couldn't send your message. Please try again."

TIMESTAMP_SALT = 'cshc.antispam.form_ts'
MIN_SUBMIT_SECONDS = 3
MAX_FORM_AGE_SECONDS = 24 * 60 * 60
MAX_MESSAGE_LENGTH = 3000
NON_LATIN_MIN_LETTERS = 20
NON_LATIN_MAX_RATIO = 0.3

# The link check is off: genuine enquiries (e.g. supplier offers) may contain links.
# Set to True to discard any message containing a link.
BLOCK_URLS = False

HONEYPOT_FIELD = 'website'
TIMESTAMP_FIELD = 'form_ts'

URL_RE = re.compile(
    r'(https?://|www\.|\[url|<a\s'
    r'|\b[a-z0-9-]+\.(ru|xyz|top|click|link|biz|online|site|shop|store|icu|buzz)\b)',
    re.IGNORECASE)

# (reason code, human-readable description) - order used for the test page summary
CHECKS = (
    ('honeypot', 'Honeypot field left empty'),
    ('missing_ts', 'Form timestamp present'),
    ('stale_or_tampered_ts', 'Form timestamp valid and less than 24 hours old'),
    ('too_fast', 'Submitted more than {} seconds after loading'.format(MIN_SUBMIT_SECONDS)),
    ('non_latin', 'Message is mostly Latin script'),
    ('too_long', 'Message is at most {} characters'.format(MAX_MESSAGE_LENGTH)),
)
URL_CHECK = ('contains_url', 'Message contains no links')


def make_timestamp():
    return signing.dumps(time.time(), salt=TIMESTAMP_SALT)


def is_mostly_non_latin(text):
    letters = [c for c in text if c.isalpha()]
    if len(letters) < NON_LATIN_MIN_LETTERS:
        return False
    # U+0000-U+024F covers Basic Latin, Latin-1 Supplement and Latin Extended-A/B
    non_latin = sum(1 for c in letters if ord(c) > 0x024F)
    return non_latin / len(letters) > NON_LATIN_MAX_RATIO


def message_spam_reasons(message):
    reasons = []
    if not message:
        return reasons
    if BLOCK_URLS and URL_RE.search(message):
        reasons.append('contains_url')
    if is_mostly_non_latin(message):
        reasons.append('non_latin')
    if len(message) > MAX_MESSAGE_LENGTH:
        reasons.append('too_long')
    return reasons


class SpamCheckFormMixin(object):
    """ Mix into a Form/ModelForm (before the form class). Fields are added in
        __init__ so this works with any form metaclass.
    """
    message_field = 'message'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.spam_reasons = []
        self.fields[HONEYPOT_FIELD] = forms.CharField(
            required=False,
            label='Leave this field blank',
            widget=forms.TextInput(attrs={'tabindex': '-1', 'autocomplete': 'off'}))
        self.fields[TIMESTAMP_FIELD] = forms.CharField(
            required=False,
            widget=forms.HiddenInput,
            initial=make_timestamp)

    def clean(self):
        cleaned_data = super().clean()
        self.spam_reasons = self._spam_reasons(cleaned_data)
        if self.spam_reasons:
            LOG.warning(
                "%s: suspected spam (%s), %s; email=%s, other form errors=%s",
                type(self).__name__, ', '.join(self.spam_reasons),
                'refused' if ENFORCE else 'allowed (log-only)',
                cleaned_data.get('email'), ', '.join(sorted(self.errors)) or 'none')
            if ENFORCE:
                raise forms.ValidationError(ENFORCED_ERROR, code='spam')
        return cleaned_data

    def _spam_reasons(self, cleaned_data):
        reasons = []
        if cleaned_data.get(HONEYPOT_FIELD):
            reasons.append('honeypot')

        token = cleaned_data.get(TIMESTAMP_FIELD)
        if not token:
            reasons.append('missing_ts')
        else:
            try:
                rendered_at = signing.loads(token, salt=TIMESTAMP_SALT, max_age=MAX_FORM_AGE_SECONDS)
                if time.time() - float(rendered_at) < MIN_SUBMIT_SECONDS:
                    reasons.append('too_fast')
            except (signing.BadSignature, TypeError, ValueError):
                # SignatureExpired is a subclass of BadSignature
                reasons.append('stale_or_tampered_ts')

        reasons.extend(message_spam_reasons(cleaned_data.get(self.message_field) or self.data.get(self.message_field, '')))
        return reasons

    def spam_check_summary(self):
        """ List of (description, passed) for each check, for diagnostics. """
        checks = CHECKS + (URL_CHECK,) if BLOCK_URLS else CHECKS
        return [(description, code not in self.spam_reasons) for code, description in checks]
