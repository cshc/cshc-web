"""
Re-usable utilities used by various CSHC apps
"""

from easy_thumbnails.files import get_thumbnailer

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


def get_thumbnail_url(image_field, profile):
    """ Gets the thumbnail URL for a given ImageField if it exists. 
        Returns None if no image field is set
    """
    if not image_field or not image_field.url:
        return None
    try:
        return get_thumbnailer(image_field)[profile].url
    except:
        return None
