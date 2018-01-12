"""
A document object wraps an uploaded file, providing some meta information about the 
file. 

Documents can be assigned a category and any number of tags.
"""

import os
from django.db import models
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager
from core.models import make_unique_filename
from .document_category import DocumentCategory
from documents import settings


def get_file_name(instance, filename):
    """ Returns a unique filename for uploaded documents."""
    filename = make_unique_filename(filename)
    return os.path.join(settings.DOCUMENTS_DIR, filename)


class DocumentManager(models.Manager):
    """ Model manager for documents """

    def by_category(self, category):
        """Returns only documents in the specified category """
        return self.get_queryset().filter(category=category)


class Document(models.Model):
    """ Represents an uploaded document """

    title = models.CharField('Document name', max_length=255)
    """ The document title """

    description = RichTextField(blank=True)
    """ Description of the document """

    timestamp = models.DateTimeField(auto_now_add=True)
    """ Timestamp to associate with this document. Can be used to order documents chronologically. """

    file = models.FileField(upload_to=get_file_name)
    """ The uploaded file """

    category = models.ForeignKey(
        DocumentCategory, on_delete=models.SET_NULL, related_name='documents', null=True, blank=True)
    """ The (optional) category to which this document belongs """

    tags = TaggableManager(blank=True)

    objects = DocumentManager()

    class Meta:
        """ Meta-info for the Award model."""
        app_label = 'documents'
        ordering = ['category', '-timestamp']

    def __str__(self):
        return str(self.title)
