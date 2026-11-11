""" Tests for the honeypot, timestamp and content anti-spam checks. """
from unittest import mock

from django import forms
from django.test import SimpleTestCase

from core import antispam
from core.antispam import SpamCheckFormMixin, make_timestamp


class SampleForm(SpamCheckFormMixin, forms.Form):
    message = forms.CharField()


class SpamCheckTests(SimpleTestCase):

    def form(self, message='Hello, I would like to come to training.', age=10, **extra):
        with mock.patch('core.antispam.time.time', return_value=1000000.0):
            timestamp = make_timestamp()
        data = {'message': message, 'form_ts': timestamp, 'website': ''}
        data.update(extra)
        form = SampleForm(data)
        with mock.patch('core.antispam.time.time', return_value=1000000.0 + age):
            self.assertTrue(form.is_valid(), form.errors)
        return form

    def test_clean_submission(self):
        form = self.form()
        self.assertEqual(form.spam_reasons, [])
        self.assertTrue(all(passed for _, passed in form.spam_check_summary()))

    def test_honeypot(self):
        self.assertIn('honeypot', self.form(website='http://spam.example').spam_reasons)

    def test_too_fast(self):
        self.assertEqual(self.form(age=1).spam_reasons, ['too_fast'])

    def test_stale_timestamp(self):
        self.assertEqual(self.form(age=antispam.MAX_FORM_AGE_SECONDS + 60).spam_reasons, ['stale_or_tampered_ts'])

    def test_tampered_timestamp(self):
        self.assertEqual(self.form(form_ts='1234567890').spam_reasons, ['stale_or_tampered_ts'])

    def test_missing_timestamp(self):
        self.assertEqual(self.form(form_ts='').spam_reasons, ['missing_ts'])

    def test_urls_allowed_by_default(self):
        form = self.form(message='Supplier offer: https://example.com/kit')
        self.assertEqual(form.spam_reasons, [])
        self.assertNotIn('Message contains no links', [d for d, _ in form.spam_check_summary()])

    @mock.patch('core.antispam.BLOCK_URLS', True)
    def test_urls_when_enabled(self):
        self.assertIn('Message contains no links', [d for d, _ in self.form().spam_check_summary()])
        for message in ('Visit https://example.com', 'see www.example.com', 'cheap at bestdeals.xyz now',
                        '[url=http://x]x[/url]', '<a href="x">x</a>'):
            with self.subTest(message=message):
                self.assertIn('contains_url', self.form(message=message).spam_reasons)

    def test_genuine_text_with_dots_is_not_a_url(self):
        message = 'I played for Cambridge City until 2019. Is there a Mens 4s team? e.g. Saturdays.'
        self.assertEqual(self.form(message=message).spam_reasons, [])

    def test_non_latin(self):
        self.assertIn('non_latin', self.form(message='Здравствуйте, предлагаем продвижение вашего сайта').spam_reasons)

    def test_accented_latin_is_fine(self):
        self.assertEqual(self.form(message='Bonjour, je m\'appelle Zoë et je voudrais jouer au hockey.').spam_reasons, [])

    def test_too_long(self):
        self.assertIn('too_long', self.form(message='a ' * 2000).spam_reasons)

    def test_log_only_by_default(self):
        with self.assertLogs('core.antispam', level='WARNING') as logs:
            form = self.form(website='filled')   # self.form() asserts the form is still valid
        self.assertEqual(form.spam_reasons, ['honeypot'])
        self.assertIn('SampleForm: suspected spam (honeypot), allowed (log-only)', logs.output[0])

    def test_clean_submission_is_not_logged(self):
        with mock.patch.object(antispam.LOG, 'warning') as warning:
            self.form()
        warning.assert_not_called()

    @mock.patch('core.antispam.ENFORCE', True)
    def test_enforced_gives_plain_error(self):
        with mock.patch('core.antispam.time.time', return_value=1000000.0):
            timestamp = make_timestamp()
        form = SampleForm({'message': 'Hello', 'form_ts': timestamp, 'website': 'filled'})
        with mock.patch('core.antispam.time.time', return_value=1000000.0 + 10),                 self.assertLogs('core.antispam', level='WARNING') as logs:
            self.assertFalse(form.is_valid())
        self.assertEqual(form.non_field_errors(), [antispam.ENFORCED_ERROR])
        self.assertNotIn('honeypot', antispam.ENFORCED_ERROR)
        self.assertIn('refused', logs.output[0])

    def test_unbound_form_has_fresh_timestamp(self):
        form = SampleForm()
        self.assertIn('form_ts', [f.name for f in form.hidden_fields()])
        self.assertTrue(form['form_ts'].value())
