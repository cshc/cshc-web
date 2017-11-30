""" Template tags for Member Offers """

from django.template import Library
from offers.models import MemberOffer

register = Library()


@register.inclusion_tag('offers/dummy.html')
def list_offers(template):
    """
    Return all active offers.
    """
    return {'template': template,
            'offers': MemberOffer.objects.active()}
