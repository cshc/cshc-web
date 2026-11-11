""" Tests for the dry-run Contact form test page. """
from unittest import mock

from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from core.antispam import make_timestamp
from core.models import ContactSubmission
from core.tests.test_turnstile import URLOPEN, fake_response


@override_settings(TURNSTILE_SITE_KEY='site-key', TURNSTILE_SECRET_KEY='secret-key')
class ContactTestPageTests(TestCase):

    def post_data(self, **extra):
        with mock.patch('core.antispam.time.time', return_value=1000000.0):
            timestamp = make_timestamp()
        data = {
            'first_name': 'Jo', 'last_name': 'Bloggs', 'email': 'jo@example.com',
            'message': 'I would like to join.', 'form_ts': timestamp, 'website': '',
            'cf-turnstile-response': 'token',
        }
        data.update(extra)
        return data

    def post(self, data, turnstile_success=True):
        with mock.patch(URLOPEN, return_value=fake_response({'success': turnstile_success})), \
                mock.patch('core.antispam.time.time', return_value=1000000.0 + 30):
            return self.client.post(reverse('contact_test'), data)

    def test_get(self):
        response = self.client.get(reverse('contact_test'))
        self.assertContains(response, 'noindex')
        self.assertContains(response, 'cf-turnstile')
        self.assertContains(response, 'name="website"')

    def test_valid_submission_is_dry_run(self):
        response = self.post(self.post_data())
        self.assertContains(response, 'Would be sent')
        self.assertEqual(ContactSubmission.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 0)

    def test_spam_submission_reports_reasons(self):
        response = self.post(self.post_data(website='filled'))
        self.assertContains(response, 'Would be sent, but logged as suspected spam: honeypot')
        self.assertContains(response, 'log-only')
        self.assertEqual(ContactSubmission.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 0)

    @mock.patch('core.antispam.ENFORCE', True)
    def test_spam_submission_when_enforced(self):
        response = self.post(self.post_data(website='filled'))
        self.assertContains(response, 'Rejected with a visible error')
        self.assertContains(response, 'enforced')
        self.assertContains(response, "couldn&#39;t send your message")
        self.assertEqual(ContactSubmission.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 0)

    def test_turnstile_failure(self):
        response = self.post(self.post_data(), turnstile_success=False)
        self.assertContains(response, 'Rejected with a visible error')
        self.assertEqual(ContactSubmission.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 0)
