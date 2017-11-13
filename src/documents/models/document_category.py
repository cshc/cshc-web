"""
Documents may optionally be in a DocumentCategory. DocumentCategories can be nested
within another parent DocumentCategory.
"""
from django.db import models


class DocumentCategoryManager(models.Manager):
    """ Model manager for document categories """

    pass


class DocumentCategory(models.Model):
    """ Represents a category of document """

    name = models.CharField("Category name", max_length=255)
    """ A user-friendly name for the document category """

    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True)
    """ The (optional) parent category """

    objects = DocumentCategoryManager()

    class Meta:
        """ Meta-info for the Award model."""
        app_label = 'documents'
        unique_together = ('name', 'parent')
        ordering = ['name']
        verbose_name_plural = "document categories"

    def __str__(self):
        return str(self.name)
