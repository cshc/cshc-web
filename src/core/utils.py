"""
Re-usable utilities used by various CSHC apps
"""

import traceback
from sorl.thumbnail import get_thumbnail
from django.conf import settings

SUFFIXES = {1: 'st', 2: 'nd', 3: 'rd'}


def ordinal(num):
    """ Returns the ordinal string from a number.

        Ref: http://codereview.stackexchange.com/a/41301
    """
    # Check for 10-20 because those are the digits that
    # don't follow the normal counting scheme.
    if 10 <= num % 100 <= 20:
        suffix = 'th'
    else:
        # the second parameter is a default.
        suffix = SUFFIXES.get(num % 10, 'th')
    return str(num) + suffix


def get_thumbnail_url(image_field, profile, cropping_field=None):
    """ Gets the thumbnail URL for a given ImageField if it exists. 
        Returns None if no image field is set
    """
    kwargs = {
        'crop': 'center',
    }
    if cropping_field and str(cropping_field) != '0x0':     # TEMP HACK
        kwargs['cropbox'] = str(cropping_field)
    if not image_field or not image_field.url:
        return None
    try:
        thumbnail_options = settings.THUMBNAIL_ALIASES[''][profile]
        im = get_thumbnail(image_field, "{}x{}".format(thumbnail_options['size'][0], thumbnail_options['size'][1]), **kwargs)
        return im.url
    except Exception as e:
        traceback.print_exc()
        return None
