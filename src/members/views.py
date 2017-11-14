"""
Views relating to CSHC Members
"""

import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from django.contrib import messages
from django.contrib.sites.models import Site
from templated_email import send_templated_mail
from competitions.models import Season
from teams.models import ClubTeam
from .models import Member
from .forms import ProfileEditForm

LOG = logging.getLogger(__name__)


class MemberListView(TemplateView):
    """ View with a list of all members"""
    template_name = 'members/member_list.html'

    def get_context_data(self, **kwargs):
        context = super(MemberListView, self).get_context_data(**kwargs)

        current_season = Season.current()
        context['props'] = {
            'currentSeason': current_season.slug,
            'teams': list(ClubTeam.objects.active().exclude(slug__in=['indoor', 'mixed']).values('long_name', 'slug')),
        }
        return context


class ProfileView(LoginRequiredMixin, UpdateView):
    """ Player profile view for a particular member.

        Provides for updating the member details via a form
        (e.g. profile pic, preferred position).

        Most player stats are loaded via a separate AJAX call.
    """
    model = Member
    template_name = 'account/profile.html'
    form_class = ProfileEditForm
    success_url = reverse_lazy('user_profile')

    def get_object(self, queryset=None):
        try:
            return Member.objects.get(user=self.request.user)
        except Member.DoesNotExist:
            return None

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        # Differentiates between this view and MemberDetailView
        context['is_profile'] = True
        context['member'] = self.get_object()
        return context

    def form_valid(self, form):
        messages.success(self.request, "Nice! Your profile has been updated.")
        return super(ProfileView, self).form_valid(form)

    def form_invalid(self, form):
        # HACK: Make use of the invalid form for handling the 'Connect my account
        # to a player' request
        if self.request.POST.get('request_link') == '1':
            try:
                send_templated_mail(
                    from_email=settings.SERVER_EMAIL,
                    recipient_list=[settings.SERVER_EMAIL],
                    template_name='req_player_link',
                    context={
                        'user': self.request.user,
                        'base_url': "//" + Site.objects.get_current().domain
                    },
                )
            except:
                LOG.error("Failed to send player link request email for {}".format(
                    self.request.user), exc_info=True)
                messages.error(
                    self.request,
                    "Sorry - we were unable to handle your request. Please try again later.")
            else:
                messages.success(
                    self.request,
                    "Thanks - your request to be linked to a player/club member has been sent to the website administrator.")
        else:
            messages.error(
                self.request,
                "Failed to update profile. Errors: {}".format(form.errors))

        return super(ProfileView, self).form_invalid(form)


class MemberDetailView(DetailView):
    """ View of a particular member"""
    model = Member

    def get_context_data(self, **kwargs):
        context = super(MemberDetailView, self).get_context_data(**kwargs)

        return context
