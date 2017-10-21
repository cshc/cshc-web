"""
Template tags for the CSHC Website
"""
from django import template
from django.contrib import messages
from django.utils.safestring import mark_safe
from graphql_relay.node.node import to_global_id

register = template.Library()

HEADING_TEMPLATE = "core/_page_heading.html"
ALERT_TEMPLATE = "blocks/_alert.html"


@register.simple_tag()
def heading(text):
    """
    Render breadcrumbs html using bootstrap css classes.
    """
    return mark_safe(template.loader.render_to_string(
        HEADING_TEMPLATE, {'title': text}))


@register.simple_tag()
def alert(alert_class, icon_class, bold_text, message, dismissable=True):
    """
    Render alert html using bootstrap css classes.
    """
    return mark_safe(template.loader.render_to_string(
        ALERT_TEMPLATE, {
            'alert_class': alert_class,
            'icon_class': icon_class,
            'bold_text': bold_text,
            'message': message,
            'dismissable': dismissable,
        }
    ))


@register.simple_tag()
def message_alert(message):
    """
    Render alert html for a Django Message using bootstrap css classes.
    """
    icon_class = "fa fa-info-circle"
    bold_text = "Heads Up!"
    if message.level == messages.SUCCESS:
        icon_class = "fa fa-check-circle-o"
        bold_text = "Success!"
    elif message.level == messages.WARNING:
        icon_class = "fa fa-exclamation-triangle"
        bold_text = "Warning!"
    elif message.level == messages.ERROR:
        icon_class = "fa fa-minus-circle"
        bold_text = "Uh-oh!"

    return mark_safe(template.loader.render_to_string(
        ALERT_TEMPLATE, {
            'alert_class': message.level_tag,
            'icon_class': icon_class,
            'bold_text': bold_text,
            'message': message.message,
            'dismissable': True,
        }
    ))


@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)


@register.filter
def graphQLId(id, type):
    """ Returns the GraphQL ID from a node type and a model ID """
    return to_global_id(type, id)
