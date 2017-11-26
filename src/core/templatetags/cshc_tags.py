"""
Template tags for the CSHC Website
"""
import logging
import codecs
import json as jsonlib
import bleach
from django import template
from django.conf import settings
from django.contrib import messages
from django.templatetags.static import static
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from graphql_relay.node.node import to_global_id
from core.models import Gender, DivisionResult, ClubInfo

register = template.Library()

LOG = logging.getLogger(__name__)


@register.inclusion_tag("core/_page_heading.html")
def heading(text):
    """
    Render a page heading.
    """
    return {'title': text}


@register.inclusion_tag("blocks/_subheading.html")
def subheading(text, id=None):
    """
    Render a subtitle.

    Ref: https://htmlstream.com/preview/unify-v2.2/unify-main/shortcodes/shortcode-base-headings.html#shortcode4-1
    """
    return {'title': text, 'subheading_id': id}


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
    level_tag = message.level_tag
    if message.level == messages.SUCCESS:
        icon_class = "fa fa-check-circle-o"
        bold_text = "Success!"
    elif message.level == messages.WARNING:
        icon_class = "fa fa-exclamation-triangle"
        bold_text = "Warning!"
    elif message.level == messages.ERROR:
        icon_class = "fa fa-minus-circle"
        bold_text = "Uh-oh!"
        level_tag = "danger"
    return alert(level_tag, icon_class, bold_text, message.message, True)


@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)


@register.filter
def formatstr(token, text):
    """ Replace '{}' with the token value """
    return text.replace("{}", token)


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
    fallback_image = 'img/kit/ladies_shirt_sq.png' if member.gender == Gender.Female else 'img/kit/mens_shirt_sq.png'
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


@register.filter()
def obfuscate(email, linktext=None, autoescape=None):
    """
    Given a string representing an email address,
        returns a mailto link with rot13 JavaScript obfuscation.

    Accepts an optional argument to use as the link text;
        otherwise uses the email address itself.
    Ref: http://djangosnippets.org/snippets/1475/

    An email address obfuscation template filter based on the ROT13 Encryption function
    in Textmate's HTML bundle.
    The filter should be applied to a string representing an email address. You can optionally
    pass the filter an argument that will be used as the email link text (otherwise it will
    simply use the email address itself).
    Example usage:
    {{ email_address|obfuscate:"Contact me!" }}
    or
    {{ email_address|obfuscate }}
    Of course, you can also use this on hardcoded email addresses, like this:
    {{ "worksology@example.com"|obfuscate }}
    """
    import re
    if autoescape:
        esc = conditional_escape
    else:
        def esc(x): return x

    try:
        email = re.sub('@', '\\\\100', re.sub('\.', '\\\\056',
                                              esc(email)))
        email = codecs.encode(email, 'rot13')
    except TypeError:
        LOG.warn("Failed to obfuscate email address")
        email = ''

    if linktext:
        linktext = codecs.encode(esc(linktext), 'rot13')
    else:
        linktext = email

    rotten_link = """<script type="text/javascript">document.write \
        ("<n uers=\\\"znvygb:%s\\\">%s<\\057n>".replace(/[a-zA-Z]/g, \
        function(c){return String.fromCharCode((c<="Z"?90:122)>=\
        (c=c.charCodeAt(0)+13)?c:c-26);}));</script>""" % (email, linktext)
    return mark_safe(rotten_link)


obfuscate.needs_autoescape = True


############################################################################################
# CLUB INFO


@register.filter()
def lookup_value(queryset, key):
    """
    Used to lookup a value from the ClubInfo table, based on the provided key.

    queryset = a QuerySet of the ClubInfo table
    key = the value of the key field of the item for which the value field is required.
    """
    try:
        return queryset.get(key=key).value
    except ClubInfo.DoesNotExist:
        return None


@register.simple_tag
def clubinfo(key):
    """A simple tag that returns the value of the given key from the ClubInfo table."""
    try:
        return ClubInfo.objects.get(key=key).value
    except ClubInfo.DoesNotExist:
        return None


@register.assignment_tag
def get_clubinfo(key):
    """An assignment version of the clubinfo tag"""
    return clubinfo(key)


@register.simple_tag
def clubinfo_email(key, linktext=None):
    """A simple tag that returns an obfuscated mailto: link to the email address matching
    the given key from the ClubInfo table."""
    return obfuscate(clubinfo(key), linktext)


clubinfo_email.needs_autoescape = True


############################################################################################
# DISQUS SUPPORT


def get_config(context):
    """
    return the formatted javascript for any disqus config variables
    """
    conf_vars = ['disqus_developer', 'disqus_identifier',
                 'disqus_url', 'disqus_title']

    output = []
    for item in conf_vars:
        if item in context:
            output.append('\tvar %s = "%s";' % (item, context[item]))
    return '\n'.join(output)


@register.inclusion_tag('disqus/recent_comments.html', takes_context=True)
def cshc_disqus_recent_comments(context, shortname='', num_items=5, excerpt_length=200, hide_avatars=0, avatar_size=32):
    """
    Return the HTML/js code which shows recent comments.

    """
    shortname = getattr(settings, 'DISQUS_WEBSITE_SHORTNAME', shortname)

    return {
        'shortname': shortname,
        'num_items': num_items,
        'hide_avatars': hide_avatars,
        'avatar_size': avatar_size,
        'excerpt_length': excerpt_length,
        'config': get_config(context),
    }
