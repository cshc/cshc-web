""" 
CSHC form widgets
"""

from django import forms
from django.conf import settings
from image_cropping import ImageCropWidget
from geoposition.widgets import GeopositionWidget


class CshcGeopositionWidget(GeopositionWidget):
    class Media:
        extend = False
        css = {
            'all': ('geoposition/geoposition.css',)
        }
        js = ('//maps.google.com/maps/api/js?key=%s' % settings.GEOPOSITION_GOOGLE_MAPS_API_KEY,
              'geoposition/geoposition.js')


class CshcCropWidget(ImageCropWidget):
    """ Override of ImageCropWidget to mitigate a bug where jQuery was being screwed up """
    class Media:
        extend = False
        css = {
            'all': ('image_cropping/css/jquery.Jcrop.min.css', 'image_cropping/css/image_cropping.css')
        }
        js = ('image_cropping/js/jquery.Jcrop.min.js',
              'image_cropping/image_cropping.js')
