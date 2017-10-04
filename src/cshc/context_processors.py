""" Context processors for the CSHC website.

    Provides common key/value pairs that will be added to the
    context of all requests.

    Ref: https://docs.djangoproject.com/en/1.11/ref/templates/api/#writing-your-own-context-processors

    Note: This requires the following TEMPLATE_CONTEXT_PROCESSOR:
        'core.context_processors.utils'
"""

from django.conf import settings

# pylint: disable=W0613


def utils(request):
    """ Returns common context items. """
    context = {
        'VERSION': settings.VERSION,
    }
    return context
