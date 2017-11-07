"""
Template tags for the CSHC Website
"""
import bleach
import json as jsonlib
from django import template
from django.template import Context
from django.contrib import messages
from django.templatetags.static import static
from django.utils.safestring import mark_safe
from graphql_relay.node.node import to_global_id
from core.models import Gender, DivisionResult

register = template.Library()


@register.inclusion_tag("core/_page_heading.html")
def heading(text):
    """
    Render breadcrumbs html using bootstrap css classes.
    """
    return {'title': text}


@register.inclusion_tag("blocks/_alert.html")
def alert(alert_class, icon_class, bold_text, message, dismissable=True):
    """
    Render alert html using bootstrap css classes.
    """
    return {
        'alert_class': alert_class,
        'icon_class': icon_class,
        'bold_text': bold_text,
        'message': message,
        'dismissable': dismissable,
    }


@register.inclusion_tag("blocks/_alert.html")
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
    return alert(message.level_tag, icon_class, bold_text, message.message, True)


@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)


@register.filter
def graphQLId(id, type):
    """ Returns the GraphQL ID from a node type and a model ID """
    return to_global_id(type, id)


@register.filter()
def urlise_model(model, linktext=None):
    """
    Given a model object,
    returns an <a> link to the model (using the model's get_absolute_url() method)

    Accepts an optional argument to use as the link text;
    otherwise uses the model's string representation
    """
    if linktext is None:
        linktext = "%s" % model

    return mark_safe("<a href='{}' title='{}'>{}</a>".format(model.get_absolute_url(), model, linktext))


@register.inclusion_tag("members/_profile_pic_thumbnail.html")
def profile_pic(member, size, className):
    """
    Given a member model, returns the HTML for a profile pic of that member.

    Parameters:
        member - the member model instance
        size - the required size of the picture (e.g. "200x200")
        className - the class to assign to the wrapper div
    """
    fallback_image = 'img/kit/Ladies%20shirt.png' if member.gender == Gender.Female else 'img/kit/Mens%20shirt.png'
    fallback_image_url = static(fallback_image)
    return {
        'member': member,
        'size': size,
        'class': className,
        'fallbackImage': fallback_image_url,
    }


@register.filter()
def strip_new_lines(text_field):
    return mark_safe(text_field.content.replace("\\r\\n", ""))


@register.filter()
def json(value):
    """safe jsonify filter, bleaches the json string using the bleach html tag remover"""
    uncleaned = jsonlib.dumps(value)
    clean = bleach.clean(uncleaned)

    try:
        jsonlib.loads(clean)
    except:
        # should never happen, but this is a last-line-of-defense check
        # to make sure this blob wont get eval'ed by the JS engine as
        # anything other than a JSON object
        raise ValueError(
            'JSON contains a quote or escape sequence that was unable to be stripped')

    return mark_safe(clean)


@register.inclusion_tag("teams/_division_result_label.html")
def division_result(part, size=None):
    """
    Render a division result
    """
    class_name = 'g-bg-black-opacity-0_1 g-color-black'
    if part.division_result in [DivisionResult.Champions, DivisionResult.Promoted]:
        class_name = 'g-bg-green'
    elif part.division_result == DivisionResult.Relegated:
        class_name = 'g-bg-red'
    if size == 'lg':
        class_name += ' u-label--lg'
    return {
        'class_name': class_name,
        'part': part,
    }
