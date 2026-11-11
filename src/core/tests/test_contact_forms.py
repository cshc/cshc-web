""" Tests for the live Contact Us and Juniors contact forms (Turnstile and anti-spam). """
from unittest import mock

from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from core.antispam import make_timestamp
from core.models import ContactSubmission, JuniorsContactSubmission
from core.tests.test_turnstile import URLOPEN, fake_response
from core.turnstile import TurnstileField
from members.forms import UnifySignupForm

MESSAGE = 'Unique message text 12345'
NOW = 1000000.0


@override_settings(TURNSTILE_SITE_KEY='site-key', TURNSTILE_SECRET_KEY='secret-key')
class LiveFormTestCase(TestCase):
    url_name = None
    model = None
    extra_data = {}

    def post_data(self, **extra):
        with mock.patch('core.antispam.time.time', return_value=NOW):
            timestamp = make_timestamp()
        data = {
            'first_name': 'Jo', 'last_name': 'Bloggs', 'email': 'jo@example.com',
            'message': MESSAGE, 'form_ts': timestamp, 'website': '',
            'cf-turnstile-response': 'token',
        }
        data.update(self.extra_data)
        data.update(extra)
        return data

    def post(self, data, turnstile_success=True):
        with mock.patch(URLOPEN, return_value=fake_response({'success': turnstile_success})) as urlopen, \
                mock.patch('core.antispam.time.time', return_value=NOW + 30):
            response = self.client.post(reverse(self.url_name), data, REMOTE_ADDR='1.2.3.4',
                                        HTTP_HOST='testserver')   # some templates need the Host header
        self.urlopen = urlopen
        return response

    def emails_to(self, address):
        return [m for m in mail.outbox if address in m.to]

    def assert_sent(self):
        self.assertEqual(self.model.objects.count(), 1)
        confirmation = self.emails_to('jo@example.com')
        self.assertEqual(len(confirmation), 1)
        # ...but the club's copy must include it
        club_copies = [m for m in mail.outbox if 'jo@example.com' not in m.to]
        self.assertEqual(len(club_copies), 1)
        self.assertIn(MESSAGE, club_copies[0].body)


class ContactFormTests(LiveFormTestCase):
    url_name = 'contact_us'
    model = ContactSubmission

    def test_get_renders_turnstile_and_honeypot(self):
        response = self.client.get(reverse(self.url_name))
        self.assertContains(response, 'class="cf-turnstile"')
        self.assertContains(response, 'class="hp-field"')
        self.assertContains(response, 'name="form_ts"')
        self.assertNotContains(response, 'g-recaptcha')

    def test_valid_submission_is_saved_and_sent(self):
        response = self.post(self.post_data())
        self.assertRedirects(response, reverse(self.url_name), fetch_redirect_response=False)
        self.assert_sent()
        posted = self.urlopen.call_args[0][0].data.decode('utf-8')
        self.assertIn('remoteip=1.2.3.4', posted)

    def test_suspected_spam_is_logged_but_still_sent(self):
        with self.assertLogs('core.antispam', level='WARNING') as logs:
            self.post(self.post_data(website='filled'))
        self.assertIn('suspected spam (honeypot), allowed (log-only)', logs.output[0])
        self.assert_sent()

    def test_turnstile_failure_is_refused(self):
        response = self.post(self.post_data(), turnstile_success=False)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'complete the verification check')
        self.assertEqual(self.model.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 0)

    @mock.patch('core.antispam.ENFORCE', True)
    def test_suspected_spam_is_refused_when_enforced(self):
        response = self.post(self.post_data(website='filled'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "couldn&#39;t send your message")
        self.assertEqual(self.model.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 0)


class JuniorsContactFormTests(LiveFormTestCase):
    url_name = 'juniors_index'
    model = JuniorsContactSubmission
    extra_data = {'child_name': 'Sam', 'child_age': 'A9', 'child_gender': 'Female', 'trigger': 'web_search'}

    def test_valid_submission_is_saved_and_sent(self):
        response = self.post(self.post_data())
        self.assertRedirects(response, reverse(self.url_name), fetch_redirect_response=False)
        self.assert_sent()

    def test_suspected_spam_is_logged_but_still_sent(self):
        with self.assertLogs('core.antispam', level='WARNING'):
            self.post(self.post_data(website='filled'))
        self.assert_sent()

    def test_turnstile_failure_is_refused(self):
        self.post(self.post_data(), turnstile_success=False)
        self.assertEqual(self.model.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 0)


class SignupFormTests(TestCase):

    def test_signup_uses_turnstile(self):
        self.assertIsInstance(UnifySignupForm.base_fields['captcha'], TurnstileField)
