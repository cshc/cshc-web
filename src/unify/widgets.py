"""
Django widgets that correspond to Unify form elements.

Refs: 
Vertical:   https://htmlstream.com/preview/unify-v2.2/unify-main/shortcodes/forms/shortcode-base-forms-unify.html
Horizontal: https://htmlstream.com/preview/unify-v2.2/unify-main/shortcodes/forms/shortcode-base-forms-horizontal-unify.html

"""

from django import forms
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string


class UnifyWidget(object):
    """ Mixin class for Unify Widgets """

    def add_classes(self, attrs, classes):
        if attrs is None:
            attrs = {}
        if 'class' not in attrs:
            attrs['class'] = classes
        else:
            attrs['class'] += ' {}'.format(classes)
        return attrs


class UnifyTextInput(UnifyWidget, forms.TextInput):
    """ Unify-styled text input widget """

    def __init__(self, attrs=None, left_icon=None, right_icon=None):
        self.left_icon = left_icon
        self.right_icon = right_icon
        attrs = self.add_classes(
            attrs, 'form-control form-control-md rounded-0')
        if left_icon:
            attrs['class'] += ' border-left-0 pl-0'
        if right_icon:
            attrs['class'] += ' border-right-0 pr-0'

        super(UnifyTextInput, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs)

        rendered_widget = super(UnifyTextInput, self).render(
            name, value, final_attrs)

        return mark_safe(render_to_string('unify/fields/text_input.html', {
            'rendered_widget': rendered_widget,
            'left_icon': self.left_icon,
            'right_icon': self.right_icon,
        }))


class UnifyTextarea(UnifyWidget, forms.Textarea):
    """ Unify-styled text area widget """

    def __init__(self, attrs=None):
        attrs = self.add_classes(
            attrs, 'form-control form-control-md rounded-0')
        super(UnifyTextarea, self).__init__(attrs)


class UnifySelect(UnifyWidget, forms.Select):
    """ Unify-styled select widget """

    def __init__(self, attrs=None):
        attrs = self.add_classes(
            attrs, 'custom-select')
        super(UnifySelect, self).__init__(attrs)


class UnifyDateTimeWidget(UnifyWidget):
    """ Unify-styled date/time widget mixin """

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs)

        rendered_widget = super(UnifyDateTimeWidget, self).render(
            name, value, final_attrs)

        return mark_safe(render_to_string('unify/fields/date_input.html', {
            'rendered_widget': rendered_widget,
        }))

    def _media(self):
        # Note: jquery-ui.min.css is required but must be included before unify.css so it is typically included
        # in the pre_link template block on any page that uses a UnifyDateTimeWidget
        return forms.widgets.Media(
            css={
                'all': []
            },
            js=[
                'vendor/jquery-ui/ui/widget.js',
                'vendor/jquery-ui/ui/version.js',
                'vendor/jquery-ui/ui/keycode.js',
                'vendor/jquery-ui/ui/position.js',
                'vendor/jquery-ui/ui/unique-id.js',
                'vendor/jquery-ui/ui/safe-active-element.js',
                'vendor/jquery-ui/ui/widgets/menu.js',
                'vendor/jquery-ui/ui/widgets/mouse.js',
                'vendor/jquery-ui/ui/widgets/datepicker.js',
                'vendor/unify/js/components/hs.datepicker.js',
                'unify/js/datetime-widget.js',
            ])

    media = property(_media)


class UnifyDateInput(UnifyDateTimeWidget, forms.DateInput):
    """ Unify-styled date input widget """

    def __init__(self, attrs=None):
        attrs = self.add_classes(attrs,
                                 'form-control form-control-md u-datepicker-v1 g-brd-right-none rounded-0 unify-datepicker')
        super(UnifyDateInput, self).__init__(attrs, format='%d-%m-%Y')
