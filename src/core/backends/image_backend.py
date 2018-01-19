"""
Custom Thumbnail backend that supports both easy-thumbnails and django-resized
"""

from image_cropping import widgets
from image_cropping.backends.base import ImageBackend
from image_cropping.backends.easy_thumbs import EasyThumbnailsBackend
from easy_thumbnails.source_generators import pil_image
from sorl.thumbnail import get_thumbnail

class ResizedImageEasyThumbnailsBackend(EasyThumbnailsBackend):
    """ Custom Thumbnail backend that supports both easy-thumbnails and django-resized """
    WIDGETS = {
        'foreign_key': widgets.CropForeignKeyWidget,
        'hidden': widgets.HiddenImageCropWidget,
        'ImageField': widgets.ImageCropWidget,
        'ImageCropField': widgets.ImageCropWidget,
        'ResizedImageField': widgets.ImageCropWidget,
    }



class ResizedImageSorlThumbnailBackend(ImageBackend):
    """ Custom Thumbnail backend that supports both sorl-thumbnail and django-resized """
    WIDGETS = {
        'foreign_key': widgets.CropForeignKeyWidget,
        'hidden': widgets.HiddenImageCropWidget,
        'ImageField': widgets.ImageCropWidget,
        'ImageCropField': widgets.ImageCropWidget,
        'ResizedImageField': widgets.ImageCropWidget,
    }

    def get_thumbnail_url(self, image_path, thumbnail_options):
        thumb = get_thumbnail(image_path, "{}x{}".format(thumbnail_options['size'][0], thumbnail_options['size'][1]), crop='center')
        return thumb.url

    def get_size(self, image):
        return pil_image(image).size