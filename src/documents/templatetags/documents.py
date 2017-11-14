"""
Template tags for Documets 
"""


from django import template
from documents.models import Document, DocumentCategory

register = template.Library()


@register.inclusion_tag("documents/_document_link.html")
def document(title, category=None):
    """
    Render a document link.
    """
    try:
        document_instance = Document.objects.get(title=title) if category is None else Document.objects.get(
            title=title, category__name=category)
    except Document.DoesNotExist:
        document_instance = None
    return {'document': document_instance}


@register.inclusion_tag("documents/_document_list.html")
def document_list(category):
    """ 
    Render a list of document links
    """
    documents = Document.objects.filter(category__name=category)
    return {
        'documents': documents,
        'category': category,
    }
