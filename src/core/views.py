""" Common Django views and view utilities
"""

import traceback
import logging
from django.views.generic.edit import CreateView, FormView
from django.contrib import messages
from django.conf import settings
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.template.loader import render_to_string
from templated_email import send_templated_mail
from competitions.models import Season
from .models import JuniorsContactSubmission, ContactSubmission, ClubInfo
from .forms import JuniorsContactSubmissionForm, ContactSubmissionForm, ContactTestForm
from . import antispam
from .antispam import HONEYPOT_FIELD, TIMESTAMP_FIELD


LOG = logging.getLogger(__name__)


def valid_kwarg(key, **dictionary):
    """ Given a key and a dictionary, returns True if the given key is in
        the dictionary and its value is not None or an empty string.
    """
    return key in dictionary and dictionary[key] is not None and dictionary[key] != ""


def kwargs_or_none(key, **dictionary):
    """ Given a key and a dictionary, returns the key's value, or None
        if the key is not valid.
    """
    if valid_kwarg(key, **dictionary):
        return dictionary[key]
    return None


def get_season_from_kwargs(kwargs):
    """ Many URLs have an optional 'season_slug' parameter, specifying
        a particular season. If not specified, we default to the current
        season.
    """
    season_slug = kwargs_or_none('season_slug', **kwargs)
    if season_slug is not None:
        season = Season.objects.get(slug=season_slug)
    else:
        season = Season.current()
    return season


def add_season_selector(context, season, season_slug_list, include_current=True):
    """ Adds season information to the given context, facilitating
        the use of the core/_season_selector.html template.

        Returns the updated context.
    """
    season_slug_list = list(dict.fromkeys(season_slug_list))
    current_season = Season.current()

    # Some views derive the selector options from historical stats/participation
    # rows, so the selected season can be missing before any data exists.
    required_slugs = [season.slug]
    if include_current:
        required_slugs.append(current_season.slug)
    if any(slug not in season_slug_list for slug in required_slugs):
        season_slug_list = list(
            Season.objects.filter(slug__in=season_slug_list + required_slugs)
            .order_by('-start')
            .values_list('slug', flat=True)
        )

    context['season'] = season
    context['current_season'] = current_season
    context['season_slug_list'] = season_slug_list
    context['base_season_slug'] = season_slug_list[0] if season_slug_list else None
    context['show_current_season_shortcut'] = current_season.slug in season_slug_list
    context['is_current_season'] = Season.is_current_season(season.id)
    return context


def site_webmanifest(request):
    """Serve the web app manifest dynamically so static URLs can vary by environment."""
    content = render_to_string(
        "site.webmanifest",
        {
            "static_url": settings.STATIC_URL,
        },
    )
    return HttpResponse(content, content_type="application/manifest+json")


class ContactSubmissionCreateView(CreateView):
    """ This is essentially the 'Contact Us' form view. """

    model = ContactSubmission
    form_class = ContactSubmissionForm
    template_name = "core/contact.html"
    success_url = reverse_lazy('contact_us')

    def email_to_secretary(self, form):
        """ Send an email to the secretary with the form data. """
        email = form.cleaned_data['email']
        context = {
            'name': u"{} {}".format(form.cleaned_data['first_name'], form.cleaned_data['last_name']),
            'phone': form.cleaned_data['phone'],
            'sender_email': email,
            'message': str(form.cleaned_data['message']),
        }

        try:
            recipient_email = ClubInfo.objects.get(key='SecretaryEmail').value
        except ClubInfo.DoesNotExist:
            recipient_email = 'secretary@cambridgesouthhockeyclub.co.uk'

        send_templated_mail(
            from_email=settings.SERVER_EMAIL,
            recipient_list=[recipient_email],
            template_name='contact_secretary',
            context=context,
            headers={'Reply-To': email},
        )

    def email_to_enquirer(self, form):
        """ Send a confirmation email to the person submitting the form. """
        context = {
            'first_name': str(form.cleaned_data['first_name']),
            'message': str(form.cleaned_data['message']),
        }
        try:
            context['secretary_name'] = ClubInfo.objects.get(
                key='SecretaryName').value
            secretary_email = ClubInfo.objects.get(
                key='SecretaryEmail').value
        except ClubInfo.DoesNotExist:
            context['secretary_name'] = ""
            secretary_email = 'secretary@cambridgesouthhockeyclub.co.uk'

        recipient_email = form.cleaned_data['email']
        send_templated_mail(
            from_email=secretary_email,
            recipient_list=[recipient_email],
            template_name='contact_sender',
            context=context,
        )

    def form_valid(self, form):
        try:
            self.email_to_secretary(form)
            self.email_to_enquirer(form)
            messages.info(
                self.request, "Thanks for your message. We'll be in touch shortly!")
        except:
            LOG.warn("Failed to send contact us email", exc_info=True)
            messages.error(
                self.request, "Sorry - we were unable to send your message. Please try again later.")
        return super(ContactSubmissionCreateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "Please enter all the required information and check the reCAPTCHA checkbox.")
        return super(ContactSubmissionCreateView, self).form_invalid(form)


class ContactTurnstileTestView(FormView):
    """ Unlisted dry-run copy of the Contact Us page, for trying out Turnstile
        and the anti-spam checks on the live site. Never saves or sends anything.
    """
    form_class = ContactTestForm
    template_name = "core/contact_test.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def results(self, form):
        turnstile = form.fields['captcha'].last_result
        turnstile_passed = 'captcha' not in form.errors
        spam_reasons = getattr(form, 'spam_reasons', [])
        if not form.is_valid():
            verdict = 'Rejected with a visible error (the user is asked to fix the form)'
        elif spam_reasons:
            verdict = 'Would be sent, but logged as suspected spam: ' + ', '.join(spam_reasons)
        else:
            verdict = 'Would be sent'
        return {
            'verdict': verdict,
            'would_send': form.is_valid(),
            'flagged': bool(spam_reasons),
            'enforced': antispam.ENFORCE,
            'turnstile_passed': turnstile_passed,
            'turnstile': turnstile,
            'turnstile_error_codes': (turnstile or {}).get('error-codes') or [],
            'spam_checks': form.spam_check_summary(),
            'form_errors': form.errors,
        }

    def form_valid(self, form):
        results = self.results(form)
        LOG.info("Turnstile test page submission: %s", results['verdict'])
        # Fresh form (new timestamp and Turnstile token), keeping what was typed
        initial = {k: v for k, v in form.cleaned_data.items()
                   if k not in ('captcha', HONEYPOT_FIELD, TIMESTAMP_FIELD)}
        new_form = self.form_class(initial=initial, request=self.request)
        return self.render_to_response(self.get_context_data(form=new_form, results=results))

    def form_invalid(self, form):
        results = self.results(form)
        LOG.info("Turnstile test page submission: %s", results['verdict'])
        return self.render_to_response(self.get_context_data(form=form, results=results))


class JuniorsContactSubmissionCreateView(CreateView):
    """ This is the enquery form for juniors. """

    model = JuniorsContactSubmission
    form_class = JuniorsContactSubmissionForm
    template_name = "club_info/juniors.html"
    success_url = reverse_lazy('juniors_index')

    def get_context_data(self, **kwargs):
        context = super(JuniorsContactSubmissionCreateView,
                        self).get_context_data(**kwargs)

        # Sub-navigation elements
        context['sub_nav_items'] = [
            {'id': 'contact-us', 'label': 'Get In Touch'},
            {'id': 'resources', 'label': 'Resources'},
            {'id': 'key_people', 'label': 'Key People'},
            {'id': 'news', 'label': 'News'},
        ]

        return context

    def email_to_juniors(self, form):
        """ Send an email to juniors@cambridgesouthhockeyclub.co.uk with the form data. """
        email = form.cleaned_data['email']
        trigger = form.cleaned_data['trigger']
        trigger_text = JuniorsContactSubmission.TRIGGER[
            trigger] if trigger != JuniorsContactSubmission.TRIGGER.not_selected else None
        context = {
            'name': u"{} {}".format(form.cleaned_data['first_name'], form.cleaned_data['last_name']),
            'phone': form.cleaned_data['phone'],
            'sender_email': email,
            'child_name': form.cleaned_data['child_name'],
            'child_age': JuniorsContactSubmission.AGE[form.cleaned_data['child_age']],
            'child_gender': JuniorsContactSubmission.GENDER[form.cleaned_data['child_gender']],
            'trigger': trigger_text,
            'message': str(form.cleaned_data['message']),
        }

        recipient_email = 'juniors@cambridgesouthhockeyclub.co.uk'
        send_templated_mail(
            from_email=settings.SERVER_EMAIL,
            recipient_list=[recipient_email],
            template_name='juniors_report',
            context=context,
            headers={'Reply-To': email},
        )

    def email_to_enquirer(self, form):
        """ Send a confirmation email to the person submitting the form. """
        context = {
            'first_name': str(form.cleaned_data['first_name']),
            'message': str(form.cleaned_data['message']),
        }

        junior_coord_name_obj, _ = ClubInfo.objects.get_or_create(
            key='JuniorsCoordName', defaults={'value': ''})
        context['juniors_coordinator_name'] = junior_coord_name_obj.value

        recipient_email = form.cleaned_data['email']
        send_templated_mail(
            from_email='juniors@cambridgesouthhockeyclub.co.uk',
            recipient_list=[recipient_email],
            template_name='juniors_sender',
            context=context,
        )

    def form_valid(self, form):
        try:
            self.email_to_juniors(form)
            self.email_to_enquirer(form)
            messages.info(
                self.request, "Thanks for your message. We'll be in touch shortly!")
        except:
            LOG.warn("Failed to send juniors email", exc_info=True)
            traceback.print_exc()
            messages.error(
                self.request, "Sorry - we were unable to send your message. Please try again later.")
        return super(JuniorsContactSubmissionCreateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "Please enter all the required information and check the reCAPTCHA checkbox.")
        return super(JuniorsContactSubmissionCreateView, self).form_invalid(form)
