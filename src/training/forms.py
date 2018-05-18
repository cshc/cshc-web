""" Custom forms related to training sessions.
"""

import logging
from datetime import timedelta, datetime
from django import forms
from core.utils import ensure_tz_aware
from unify.widgets import (
    UnifyTextInput,
    UnifySelect,
    UnifyDateInput,
    UnifyNumericInput,
    UnifyTimeInput,
    UnifyTextarea,
    UnifyRadioInput)
from venues.models import Venue
from .models import TrainingSession

LOG = logging.getLogger(__name__)

NO_REPEAT = 'N'
MULTIPLE = 'M'
UNTIL = 'U'
REPEAT_CHOICES = (
    (NO_REPEAT, "One-off"),
    (MULTIPLE, "Multiple"),
    (UNTIL, "Until")
)

DATE_INPUT_FORMATS = ['%Y-%m-%d', '%d/%m/%Y',
                      '%d-%m-%Y', '%d/%m/%y', '%d-%m-%y']
TIME_INPUT_FORMATS = ['%H:%M']


class TrainingSessionForm(forms.Form):
    """ A custom form for adding multiple training sessions. """

    venue = forms.ModelChoiceField(
        queryset=Venue.objects.home_venues(), widget=UnifySelect)

    description = forms.CharField(
        min_length=2, max_length=200, widget=UnifyTextarea(attrs={'rows': '3'}))

    # Need localize=True to ensure TextInput is the base widget expected
    duration_mins = forms.IntegerField(label="Duration (mins)", localize=True,
                                       initial=90, min_value=10, max_value=480,
                                       widget=UnifyNumericInput)

    date = forms.DateField(input_formats=DATE_INPUT_FORMATS,
                           initial=datetime.now(), widget=UnifyDateInput(attrs={'class': 'g-width-120'}))
    time = forms.TimeField(initial="19:00",
                           input_formats=TIME_INPUT_FORMATS, widget=UnifyTimeInput(attrs={'class': 'g-width-120'}))

    # NOTE: The HTML template (training/trainingsession_form.html) for the repeat_* fields is 'hard-coded'.
    # Not all of the values shown here will be respected.
    repeat_option = forms.ChoiceField(label="Repeat", choices=REPEAT_CHOICES,
                                      widget=UnifyRadioInput)

    repeat_count = forms.IntegerField(
        label="",
        min_value=2, max_value=52, initial=10, required=False,
        widget=UnifyNumericInput)

    repeat_until = forms.DateField(
        label="",
        input_formats=DATE_INPUT_FORMATS, required=False, widget=UnifyDateInput(attrs={'class': 'g-width-120'}))

    def save_training_sessions(self):
        """ Save the training sessions specified by the form data. """
        if self.cleaned_data['repeat_option'] == NO_REPEAT:
            LOG.info("Saving a single training session")
            return [self.new_session()]
        else:
            # Save multiple training sessions
            sessions = []
            if self.cleaned_data['repeat_option'] == MULTIPLE:
                LOG.info("Saving {} repeated training sessions".format(
                    self.cleaned_data['repeat_count']))
                for i in range(0, self.cleaned_data['repeat_count']):
                    sessions.append(self.new_session(i))
            else:
                LOG.info("Saving repeated training sessions up to {}".format(
                    self.cleaned_data['repeat_until']))
                week_offset = 0
                start_date = self.cleaned_data['date']
                end = self.cleaned_data['repeat_until']
                while end > (start_date + timedelta(days=week_offset*7)):
                    sessions.append(self.new_session(week_offset))
                    week_offset += 1
            return sessions

    def new_session(self, week_offset=0):
        """ Adds a new training session at the specified week offset. """
        session = TrainingSession()
        session.venue = self.cleaned_data['venue']
        session.description = self.cleaned_data['description']
        session.datetime = ensure_tz_aware(datetime.combine(
            self.cleaned_data['date'] + timedelta(days=week_offset*7),
            self.cleaned_data['time']))
        session.duration_mins = self.cleaned_data['duration_mins']
        session.save()
        return session
