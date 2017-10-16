"""
Template tags for the CSHC Website
"""
from django import template
from django.utils.safestring import mark_safe
from graphql_relay.node.node import to_global_id

register = template.Library()

HEADING_TEMPLATE = "core/_page_heading.html"


@register.simple_tag()
def heading(text):
    """
    Render breadcrumbs html using bootstrap css classes.
    """
    return mark_safe(template.loader.render_to_string(
        HEADING_TEMPLATE, {'title': text}))


@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)


@register.filter
def graphQLId(id, type):
    """ Returns the GraphQL ID from a node type and a model ID """
    return to_global_id(type, id)
