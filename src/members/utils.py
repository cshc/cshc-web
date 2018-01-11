"""
Utility methods for Members
"""

from .models import Member


def member_from_request(request):
    """ Returns the Member object corresponding to the authenticated user - if there is one. """
    try:
        if request.user.is_authenticated():
            return Member.objects.only('id').get(user_id=request.user.id)
        else:
            return None
    except Member.DoesNotExist:
        return None
