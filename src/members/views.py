"""
Views relating to CSHC Members
"""

import logging
import copy
import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import UpdateView
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.contrib import messages
from django.contrib.sites.models import Site
from django.http import JsonResponse
from templated_email import send_templated_mail
from core.models import CshcUser
from core.forms import UserProfileForm
from core.utils import get_thumbnail_url
from competitions.models import Season
from teams.models import ClubTeam
from .models import Member
from .forms import MemberProfileForm

LOG = logging.getLogger(__name__)


def js_members():
    """
    Return a list of all members, with id and name properties,
    suitable for passing to JavaScript.
    """
    return [{'id': x.id, 'name': x.full_name()} for x in Member.objects.only('id', 'first_name', 'known_as', 'last_name')]


class MemberListView(TemplateView):
    """ View with a list of all members"""
    template_name = 'members/member_list.html'

    def get_context_data(self, **kwargs):
        context = super(MemberListView, self).get_context_data(**kwargs)

        current_season = Season.current()
        context['props'] = {
            'canViewMap': self.request.user.has_perm('members.view_personal_data'),
            'currentSeason': current_season.slug,
            'teams': list(ClubTeam.objects.active().values('long_name', 'slug')),
            'seasons': list(Season.objects.all().order_by('-slug').values_list('slug', flat=True)),
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
                'base_url': "https://" + Site.objects.get_current().domain,
                'members_admin_url': "{}?q={}".format(reverse('admin:members_member_changelist'), request.user.get_full_name())
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
    try:
        context['link_req_sent'] = int(request.COOKIES.get(
            link_req_cookie, 0))
    except ValueError:
        context['link_req_sent'] = 0

    if request.method == 'POST':
        if request.POST.get('request_link') == '1':
            # This is a request to link the authenticated user to a member.
            context['form'] = UserProfileForm(instance=request.user)
            try:
                success = send_link_req(request)
                if success:
                    context['link_req_sent'] = 1
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
                messages.error(
                    request,
                    "Profile could not be updated. See individual fields for details.")
                context['form'] = form
        else:
            # This is a User with an associated Member. Use the MemberProfileForm.
            form = MemberProfileForm(
                request.POST, request.FILES, instance=member)
            if form.is_valid():
                updated_member = form.save()
                messages.success(
                    request,
                    "Your profile has been updated successfully")
                context['form'] = MemberProfileForm(instance=updated_member)
                context['form'].fields['dob'].initial = updated_member.dob
            else:
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
                    context['link_req_sent'] = 1
            except CshcUser.DoesNotExist:
                pass

        # Create the appropriate form, populated with the model data
        context['form'] = MemberProfileForm(
            instance=member) if member is not None else UserProfileForm(instance=request.user)

    response = render(request, 'account/profile.html', context)
    response.set_cookie(link_req_cookie, context.get('link_req_sent', 0))
    return response


@login_required
@require_GET
def get_available_shirt_numbers(request):
    """
    AJAX endpoint to get available *numerical* shirt numbers for the current user's gender.
    Returns a JSON response with a list of numbers.
    """
    member = getattr(request.user, 'member', None)
    if not member:
        return JsonResponse({'error': 'User is not associated with a member profile.'}, status=400)

    if not member.gender:
        return JsonResponse({'error': 'Member gender not specified. Cannot determine available shirt numbers.'}, status=400)

    # Use the manager method to fetch available numbers
    # The limit will come from settings by default, or can be overridden here if needed
    available_numbers = Member.objects.get_available_shirt_numbers(member.gender)
    return JsonResponse({'available_numbers': available_numbers})


@login_required
@require_POST
def assign_shirt_number(request):
    """
    AJAX endpoint to assign a selected *numerical* shirt number to the current user's member profile.
    Expects a POST request with JSON data containing 'shirt_number'.
    """
    member = getattr(request.user, 'member', None)
    if not member:
        return JsonResponse({'error': 'User is not associated with a member profile.'}, status=400)

    try:
        data = json.loads(request.body)
        selected_number_int = int(data.get('shirt_number')) # Get as int for validation
    except (json.JSONDecodeError, TypeError, ValueError):
        return JsonResponse({'error': 'Invalid data provided.'}, status=400)

    # Basic validation for typical shirt numbers
    if not (1 <= selected_number_int <= 999): # Allowing up to 3 digits, adjust as per MEMBERS_MAX_SHIRT_NUMBER
        return JsonResponse({'error': 'Invalid shirt number. Must be a positive integer.'}, status=400)

    if not member.gender:
        return JsonResponse({'error': 'Member gender not specified. Cannot assign shirt number.'}, status=400)

    # Robust check: ensure the number is still available for this gender
    # We fetch all available numbers (limit=None) to be sure, not just the first few.
    if selected_number_int not in Member.objects.get_available_shirt_numbers(member.gender, limit=None):
        return JsonResponse({'error': f'Shirt number {selected_number_int} is no longer available for your gender or is invalid.'}, status=400)

    # Convert to string before saving to CharField
    selected_number_str = str(selected_number_int)

    # Check if the number is already assigned to *this* member (no change needed)
    if member.shirt_number == selected_number_str:
        return JsonResponse({'message': f'Shirt number {selected_number_str} is already assigned to you.'}, status=200)

    # Assign the number and save
    member.shirt_number = selected_number_str
    member.save()

    return JsonResponse({'message': f'Shirt number {selected_number_str} successfully assigned.'})


class MemberDetailView(DetailView):
    """ View of a particular member"""
    model = Member

    def get_context_data(self, **kwargs):
        context = super(MemberDetailView, self).get_context_data(**kwargs)
        member = context['member']

        current_squad = member.current_squad()
        squad = dict(slug=current_squad.team.slug,
                     name=current_squad.team.long_name) if current_squad is not None else None

        is_me = (self.request.user.is_authenticated and
                 self.request.user.has_member() and
                 self.request.user.member.id == member.id)

        context['props'] = dict(
            isMe=is_me,
            member=dict(
                id=member.id,
                firstName=member.pref_first_name(),
                lastName=member.last_name,
                profilePicUrl=get_thumbnail_url(
                    member.profile_pic, '255x255', 'center', member.profile_pic_cropping),
                prefPosition=member.get_pref_position_display(),
                squad=squad,
                isUmpire=member.is_umpire,
            ),
        )
        return context
