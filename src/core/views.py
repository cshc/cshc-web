""" Common Django views and view utilities
"""

import traceback
import logging
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.urls import reverse_lazy
from templated_email import send_templated_mail
from competitions.models import Season
from .models import JuniorsContactSubmission, ContactSubmission, ClubInfo
from .forms import JuniorsContactSubmissionForm, ContactSubmissionForm


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


def add_season_selector(context, season, season_list):
    """ Adds season information to the given context, facilitating
        the use of the core/_season_selector.html template.

        Returns the updated context.
    """
    context['season'] = season
    context['season_list'] = season_list
    context['is_current_season'] = Season.is_current_season(season.id)
    return context


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
            'join_mail_list': form.cleaned_data['mailing_list'],
            'message': str(form.cleaned_data['message']),
        }

        try:
            recipient_email = ClubInfo.objects.get(key='SecretaryEmail').value
        except ClubInfo.DoesNotExist:
            recipient_email = 'secretary@cambridgesouthhockeyclub.co.uk'

        send_templated_mail(
            from_email=email,
            recipient_list=[recipient_email],
            template_name='contact_secretary',
            context=context,
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
            context['secretary_email'] = ClubInfo.objects.get(
                key='SecretaryEmail').value
        except ClubInfo.DoesNotExist:
            context['secretary_name'] = ""
            context['secretary_email'] = 'secretary@cambridgesouthhockeyclub.co.uk'

        recipient_email = form.cleaned_data['email']
        send_templated_mail(
            from_email=context['secretary_email'],
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
            {'id': 'contacts', 'label': 'Contacts'},
            {'id': 'resources', 'label': 'Resources'},
            {'id': 'calendar', 'label': 'Calendar'},
            {'id': 'news', 'label': 'News'},
            {'id': 'contact-us', 'label': 'Get In Touch'},
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
            'join_mail_list': form.cleaned_data['mailing_list'],
            'message': str(form.cleaned_data['message']),
        }

        recipient_email = 'juniors@cambridgesouthhockeyclub.co.uk'
        send_templated_mail(
            from_email=email,
            recipient_list=[recipient_email],
            template_name='juniors_report',
            context=context,
        )

    def email_to_enquirer(self, form):
        """ Send a confirmation email to the person submitting the form. """
        context = {
            'first_name': str(form.cleaned_data['first_name']),
            'message': str(form.cleaned_data['message']),
        }

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
