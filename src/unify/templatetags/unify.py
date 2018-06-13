
from django import template
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string

register = template.Library()


@register.inclusion_tag("unify/forms/section_heading.html")
def unify_form_section_heading(heading):
    """
    Render a form section heading.
    """
    return {'heading': heading}


@register.simple_tag
def unify_form_submit_button(text, orientation='vertical', name=None):
    """
    Render a form submit button.
    """
    button_template = 'unify/forms/{}/submit.html'.format(orientation)
    return mark_safe(render_to_string(button_template, {'text': text, 'name': name}))


@register.inclusion_tag("unify/forms/section_divider.html")
def unify_form_section_divider():
    """
    Render a form section divider.
    """
    return {}


@register.simple_tag
def unify_form_required_fields_footnote(orientation='vertical'):
    """
    Render a form section divider.
    """
    footnote_template = 'unify/forms/{}/required_fields_footnote.html'.format(
        orientation)
    return mark_safe(render_to_string(footnote_template))


@register.inclusion_tag("unify/forms/non_field_errors.html", takes_context=True)
def unify_form_non_field_errors(context):
    """
    Render errors on a form that are not associated with a particular field.
    """
    return {'errors': context['form'].non_field_errors}


@register.simple_tag(takes_context=True)
def unify_form_field(context, field_name, orientation='vertical', hide_label=False, **extra_context):
    """
    Render Unify form field
    """
    field_template = 'unify/forms/{}/field.html'.format(orientation)
    form = context['form']
    if 'label_class' not in extra_context:
        extra_context['label_class'] = 'sr-only'
    return mark_safe(render_to_string(field_template, {
        'label': form[field_name].label if not hide_label else None,
        'field': form[field_name],
        **extra_context,
    }))


@register.simple_tag(takes_context=True)
def unify_cropped_image_form_field(context, field_name, cropping_field_name, orientation='vertical', hide_label=False):
    """
    Render Unify form field for a cropped image
    """
    field_template = 'unify/forms/{}/cropping_image_field.html'.format(
        orientation)
    form = context['form']
    return mark_safe(render_to_string(field_template, {
        'label': form[field_name].label if not hide_label else None,
        'field': form[field_name],
        'cropping_field': form[cropping_field_name],
    }))
