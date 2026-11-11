""" Tests for the Cloudflare Turnstile form field and widget. """
import io
import json
import socket
from unittest import mock
from urllib.error import HTTPError, URLError

from django import forms
from django.test import SimpleTestCase, override_settings

from core.turnstile import TurnstileField, get_client_ip

URLOPEN = 'core.turnstile.urlopen'


def fake_response(payload):
    body = payload if isinstance(payload, bytes) else json.dumps(payload).encode('utf-8')
    response = io.BytesIO(body)
    return response   # BytesIO supports the context manager protocol and read()


@override_settings(TURNSTILE_SITE_KEY='site-key', TURNSTILE_SECRET_KEY='secret-key')
class TurnstileFieldTests(SimpleTestCase):

    def clean(self, token='token', remote_ip=None):
        field = TurnstileField()
        field.remote_ip = remote_ip
        try:
            field.clean(token)
            return field, None
        except forms.ValidationError as ex:
            return field, ex

    def test_success(self):
        with mock.patch(URLOPEN, return_value=fake_response({'success': True, 'hostname': 'example.com'})) as urlopen:
            field, error = self.clean(remote_ip='1.2.3.4')
        self.assertIsNone(error)
        self.assertEqual(field.last_result['hostname'], 'example.com')
        posted = urlopen.call_args[0][0].data.decode('utf-8')
        self.assertIn('secret=secret-key', posted)
        self.assertIn('response=token', posted)
        self.assertIn('remoteip=1.2.3.4', posted)

    def test_failure(self):
        with mock.patch(URLOPEN, return_value=fake_response({'success': False, 'error-codes': ['invalid-input-response']})):
            field, error = self.clean()
        self.assertEqual(error.code, 'invalid')
        self.assertEqual(field.last_result['error-codes'], ['invalid-input-response'])

    def test_missing_token(self):
        with mock.patch(URLOPEN) as urlopen:
            _, error = self.clean(token='')
        self.assertEqual(error.code, 'required')
        urlopen.assert_not_called()

    def test_network_errors_become_validation_errors(self):
        errors = [
            socket.timeout('timed out'),
            URLError('dns failure'),
            HTTPError('https://x', 500, 'Server Error', {}, None),
        ]
        for exc in errors:
            with self.subTest(exc=type(exc).__name__):
                with mock.patch(URLOPEN, side_effect=exc):
                    field, error = self.clean()
                self.assertEqual(error.code, 'unavailable')
                self.assertTrue(field.last_result['unavailable'])

    def test_bad_json(self):
        with mock.patch(URLOPEN, return_value=fake_response(b'<html>not json</html>')):
            _, error = self.clean()
        self.assertEqual(error.code, 'unavailable')

    def test_widget_renders_site_key(self):
        html = TurnstileField().widget.render('captcha', None)
        self.assertIn('class="cf-turnstile"', html)
        self.assertIn('data-sitekey="site-key"', html)
        self.assertIn('data-theme="light"', html)
        self.assertIn('challenges.cloudflare.com/turnstile/v0/api.js', html)

    def test_widget_reads_turnstile_param(self):
        value = TurnstileField().widget.value_from_datadict({'cf-turnstile-response': 'abc'}, {}, 'captcha')
        self.assertEqual(value, 'abc')

    def test_client_ip(self):
        request = mock.Mock(META={'HTTP_X_FORWARDED_FOR': '5.6.7.8, 10.0.0.1', 'REMOTE_ADDR': '10.0.0.1'})
        self.assertEqual(get_client_ip(request), '5.6.7.8')
        request = mock.Mock(META={'REMOTE_ADDR': '10.0.0.2'})
        self.assertEqual(get_client_ip(request), '10.0.0.2')
        self.assertIsNone(get_client_ip(None))
