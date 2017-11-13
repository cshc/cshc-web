""" Configuration of Documents models for the Django admin interface.
"""

from django.contrib import admin
from .models import Document, DocumentCategory


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """ Admin interface definition for the Document model. """
    search_fields = ('title', 'description')
    list_display = ('title', 'category', 'tag_list')
    list_filter = ('category',)

    def get_queryset(self, request):
        return super(DocumentAdmin, self).get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())


@admin.register(DocumentCategory)
class DocumentCategoryAdmin(admin.ModelAdmin):
    """ Admin interface definition for the DocumentCategory model. """

    list_display = ('name', 'parent')
