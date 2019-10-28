""" Context processors for the CSHC website.

    Provides common key/value pairs that will be added to the
    context of all requests.

    Ref: https://docs.djangoproject.com/en/1.11/ref/templates/api/#writing-your-own-context-processors

    Note: This requires the following TEMPLATE_CONTEXT_PROCESSOR:
        'core.context_processors.utils'
"""

from django.conf import settings
from members.utils import member_from_request

# pylint: disable=W0613


def utils(request):
    """ Returns common context items. """
    member = member_from_request(request)
    context = {
        'member_id': member.id if member else None,
        'VERSION': settings.VERSION,
        'STATIC_URL': settings.STATIC_URL,
        "GMAPS_API_KEY": settings.GMAPS_API_KEY,
        "ENABLE_AVAILABILITY": settings.AVAILABILITY_ENABLED,
        'TEAMS': [
            {
                'title': 'Mens',
                'list': [
                    ('m1', 'Mens 1sts',),
                    ('m2', 'Mens 2nds',),
                    ('m3', 'Mens 3rds',),
                    ('m4', 'Mens 4ths',),
                    ('m5', 'Mens 5ths',),
                    ('m6', 'Mens 6ths',),
                    # Add a border above this item
                    ('m-in', 'Mens Indoor', True),
                    ('mv', 'Mens Vets',),
                ],
            },
            {
                'title': 'Ladies',
                'list': [
                    ('l1', 'Ladies 1sts',),
                    ('l2', 'Ladies 2nds',),
                    ('l3', 'Ladies 3rds',),
                    ('l4', 'Ladies 4ths',),
                    ('l5', 'Ladies 5ths',),
                    # Add a border above this item
                    ('l-in', 'Ladies Indoor', True),
                    # ('lv', 'Ladies Vets',),
                ],
            },
            {
                'title': 'Other',
                'list': [
                    ('mixed', 'Mixed',),
                ],
            },
        ],
    }
    return context
