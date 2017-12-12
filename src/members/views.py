"""
Views relating to CSHC Members
"""

import logging
import copy
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from django.contrib import messages
from django.contrib.sites.models import Site
from templated_email import send_templated_mail
from core.models import CshcUser
from core.forms import UserProfileForm
from core.utils import get_thumbnail_url
from competitions.models import Season
from teams.models import ClubTeam
from .models import Member
from .forms import MemberProfileForm

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


def send_link_req(request):
    """ Send a player link request email to the website admin """
    try:
        send_templated_mail(
            from_email=settings.SERVER_EMAIL,
            recipient_list=[settings.SERVER_EMAIL],
            template_name='req_player_link',
            context={
                'user': request.user,
                'base_url': "//" + Site.objects.get_current().domain
            },
        )
    except:
        LOG.error("Failed to send player link request email for {}".format(
            request.user), exc_info=True, extra={'request': request})
        messages.error(
            request,
            "Sorry - we were unable to handle your request. Please try again later.")
        return False
    else:
        messages.success(
            request,
            "Thanks - your request to be linked to a player/club member has been sent to the website administrator.")
        return True


@login_required
def profile(request):
    link_req_cookie = 'link_req_sent-{}'.format(request.user.id)
    context = {}
    kwargs = dict(user=request.user)
    member = Member.objects.safe_get(**kwargs)
    context['member'] = member

    # We store the fact that the user has requested to be linked to a Member in a cookie
    # This way we don't show the link request again (on the same browser) once they've clicked on it
    context['link_req_sent'] = request.COOKIES.get(
        link_req_cookie, None)

    if request.method == 'POST':
        if request.POST.get('request_link') == '1':
            # This is a request to link the authenticated user to a member.
            context['form'] = UserProfileForm(instance=request.user)
            try:
                success = send_link_req(request)
                if success:
                    context['link_req_sent'] = True
            except CshcUser.DoesNotExist:
                pass
        elif request.POST.get('no_member') == '1':
            # This is a User with no member associated. So we should use the UserProfileForm.
            form = UserProfileForm(request.POST, instance=request.user)
            if form.is_valid():
                updated_user = form.save()
                messages.success(
                    request,
                    "Your profile has been updated successfully")
                context['form'] = UserProfileForm(instance=updated_user)
            else:
                print('Invalid', form.errors)
                messages.error(
                    request,
                    "Profile could not be updated. See individual fields for details.")
                context['form'] = form
        else:
            # This is a User with an associated Member. Use the MemberProfileForm.
            print('dob', request.POST.get('dob'))
            form = MemberProfileForm(
                request.POST, request.FILES, instance=member)
            print('MemberProfileForm created with POST')
            if form.is_valid():
                updated_member = form.save()
                print('dob-updated', updated_member.dob)
                messages.success(
                    request,
                    "Your profile has been updated successfully")
                context['form'] = MemberProfileForm(instance=updated_member)
                context['form'].fields['dob'].initial = updated_member.dob
                print('MemberProfileForm created with just instance')
            else:
                print('Invalid', form.errors)
                messages.error(
                    request,
                    "Profile could not be updated. See individual fields for details.")
                context['form'] = form

    else:
        # if req_link is supplied in the url params, trigger the player link request now
        req_link_id = request.GET.get('req_link_id')
        if not member and not context['link_req_sent'] and req_link_id is not None:
            try:
                success = send_link_req(request)
                if success:
                    context['link_req_sent'] = True
            except CshcUser.DoesNotExist:
                pass

        # Create the appropriate form, populated with the model data
        context['form'] = MemberProfileForm(
            instance=member) if member is not None else UserProfileForm(instance=request.user)

    response = render(request, 'account/profile.html', context)
    response.set_cookie(link_req_cookie, context.get('link_req_sent', False))
    return response


class MemberDetailView(DetailView):
    """ View of a particular member"""
    model = Member

    def get_context_data(self, **kwargs):
        context = super(MemberDetailView, self).get_context_data(**kwargs)
        member = context['member']

        current_squad = member.current_squad()
        squad = dict(slug=current_squad.team.slug,
                     name=current_squad.team.long_name) if current_squad is not None else None

        context['props'] = dict(
            member=dict(
                id=member.id,
                firstName=member.first_name,
                lastName=member.last_name,
                profilePicUrl=get_thumbnail_url(
                    member.profile_pic, 'member_detail'),
                prefPosition=member.get_pref_position_display(),
                squad=squad,
            ),
        )
        return context
