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
    template_name = 'unify/fields/text_input.html'

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

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['left_icon'] = self.left_icon
        context['right_icon'] = self.right_icon
        return context


class UnifyPhoneInput(UnifyTextInput):
    """ Unify-styled telephone input widget """
    input_type = 'tel'

    def __init__(self, attrs=None):
        super(UnifyPhoneInput, self).__init__(attrs, 'fas fa-phone')


class UnifyTimeInput(UnifyWidget, forms.TimeInput):
    """ Unify-styled time input widget """
    input_type = 'time'
    template_name = 'unify/fields/text_input.html'

    def __init__(self, attrs=None):
        attrs = self.add_classes(
            attrs, 'form-control form-control-md rounded-0')

        super(UnifyTimeInput, self).__init__(attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['right_icon'] = 'icon-clock'
        context['input_group_class'] = 'g-width-170'
        return context


class UnifyNumericInput(UnifyWidget, forms.NumberInput):
    """ Unify-styled numeric input widget """
    input_type = 'text'
    template_name = 'unify/fields/numeric_input.html'

    def __init__(self, attrs=None):
        attrs = self.add_classes(
            attrs, 'js-result form-control text-center rounded-0 g-pa-15')
        super(UnifyNumericInput, self).__init__(attrs)

    def _media(self):
        # Note: jquery-ui.min.css is required but must be included before unify.css so it is typically included
        # in the pre_link template block on any page that uses a UnifyDateTimeWidget
        return forms.widgets.Media(
            css={
                'all': [
                    'vendor/themify-icons/themify-icons.css',
                ]
            },
            js=[
                'unify/js/hs.count-qty.js',
                'unify/js/quantity.js',
            ])

    media = property(_media)


class UnifyTextarea(UnifyWidget, forms.Textarea):
    """ Unify-styled text area widget """

    def __init__(self, attrs=None):
        attrs = self.add_classes(
            attrs, 'form-control form-control-md rounded-0')
        super(UnifyTextarea, self).__init__(attrs)


class UnifyCheckboxInput(UnifyWidget, forms.CheckboxInput):
    """ Unify-styled checkbox widget """
    template_name = 'unify/fields/checkbox_input.html'

    def __init__(self, attrs=None, label=''):
        self.label = label
        attrs = self.add_classes(
            attrs, 'g-hidden-xs-up g-pos-abs g-top-0 g-left-0')
        super(UnifyCheckboxInput, self).__init__(attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['label'] = self.label
        return context


class UnifyRadioInput(UnifyWidget, forms.RadioSelect):
    """ Unify-styled radio widget """
    option_template_name = 'unify/fields/radio_input.html'

    def __init__(self, attrs=None):
        attrs = self.add_classes(
            attrs, 'list-unstyled')
        super(UnifyRadioInput, self).__init__(attrs)

    def create_option(self, *args, **kwargs):
        context = super().create_option(*args, **kwargs)
        widget_attrs = context['attrs']
        widget_attrs = self.add_classes(
            widget_attrs, 'g-hidden-xs-up g-pos-abs g-top-0 g-left-0')
        return context


class UnifySelect(UnifyWidget, forms.Select):
    """ Unify-styled select widget """

    def __init__(self, attrs=None):
        attrs = self.add_classes(
            attrs, 'custom-select')
        super(UnifySelect, self).__init__(attrs)


class UnifyDateTimeWidget(UnifyWidget):
    """ Unify-styled date/time widget mixin """
    template_name = 'unify/fields/date_input.html'

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
                'js/hs.datepicker.custom.js',
                'unify/js/datetime-widget.js',
            ])

    media = property(_media)


class UnifyDateInput(UnifyDateTimeWidget, forms.DateInput):
    """ Unify-styled date input widget """

    def __init__(self, attrs=None):
        attrs = self.add_classes(attrs,
                                 'form-control form-control-md u-datepicker-v1 g-brd-right-none rounded-0 unify-datepicker')
        super(UnifyDateInput, self).__init__(attrs, format='%d-%m-%Y')
