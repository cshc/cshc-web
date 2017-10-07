"""
Custom Thumbnail backend that supports both easy-thumbnails and django-resized
"""

from image_cropping import widgets
from image_cropping.backends.easy_thumbs import EasyThumbnailsBackend


class ResizedImageEasyThumbnailsBackend(EasyThumbnailsBackend):
    """ Custom Thumbnail backend that supports both easy-thumbnails and django-resized """
    WIDGETS = {
        'foreign_key': widgets.CropForeignKeyWidget,
        'hidden': widgets.HiddenImageCropWidget,
        'ImageField': widgets.ImageCropWidget,
        'ImageCropField': widgets.ImageCropWidget,
        'ResizedImageField': widgets.ImageCropWidget,
    }
