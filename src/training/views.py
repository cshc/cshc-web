"""
Views for Training Sessions
"""

import logging
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import transaction
from braces.views import SelectRelatedMixin, LoginRequiredMixin, PermissionRequiredMixin
from .models import TrainingSession
from .forms import TrainingSessionForm


LOG = logging.getLogger(__name__)

# The max number of upcoming training sessions to display
MAX_SESSIONS_TO_DISPLAY = 5


class UpcomingTrainingSessionsView(ListView):
    """View for a list of upcoming training sessions"""

    model = TrainingSession

    queryset = TrainingSession.objects.upcoming().select_related('venue')[
        :MAX_SESSIONS_TO_DISPLAY]

    @staticmethod
    def addUpcomingTrainingToContext(context):
        """ Utility method to add upcoming training session data to the
            given context. Useful when embedding a list of upcoming training
            sessions on other pages.
        """
        context['trainingsession_list'] = UpcomingTrainingSessionsView.queryset


class TrainingSessionDetailView(SelectRelatedMixin, DetailView):
    """View for the details of a training session"""
    model = TrainingSession
    select_related = ['venue']


class TrainingSessionFormView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    """ View for creating new training sessions. """
    template_name = 'training/trainingsession_form.html'
    form_class = TrainingSessionForm
    permission_required = "training.add_trainingsession"
    success_url = reverse_lazy('trainingsession_create')

    def form_valid(self, form):
        try:
            with transaction.atomic():
                sessions = form.save_training_sessions()
                messages.info(self.request, "Saved {} new training session{}".format(
                    len(sessions), "s" if len(sessions) > 1 else ""))
        except Exception as ex:
            LOG.error("Failed to save training sessions: {}".format(
                ex), exc_info=True)
            messages.error(
                self.request, "Failed to save training sessions. Please check the details.")
        return super(TrainingSessionFormView, self).form_valid(form)

    def form_invalid(self, form):
        response = super(TrainingSessionFormView, self).form_invalid(form)
        LOG.error("Form is invalid: {}".format(form))
        return response
