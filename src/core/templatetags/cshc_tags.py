"""
Template tags for the CSHC Website
"""
import logging
import codecs
import os
import re
import traceback
import json as jsonlib
import bleach
from django import template
from django.contrib import messages
from django.conf import settings
from django.templatetags.static import static
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from fluent_comments.models import FluentComment
from graphql_relay.node.node import to_global_id
from zinnia.models.entry import Entry
from core.models import Gender, DivisionResult, ClubInfo

register = template.Library()

LOG = logging.getLogger(__name__)


@register.simple_tag(takes_context=True)
def abs_static_url(context, url):
    """ Get the absolute URL of a static resource """
    if re.match('(http:|https:)?//', settings.STATIC_URL):
        return ''.join([settings.STATIC_URL, url])
    return ''.join(["http://", context.request.META['HTTP_HOST'], settings.STATIC_URL, url])


@register.simple_tag
def social_provider_icon(provider_id):
    """ Returns the appropriate (fontawesome) icon class for a Social Account Provider ID """
    if provider_id == 'facebook':
        return 'fab fa-facebook-f'
    if provider_id == 'linkedin_oauth2':
        return 'fab fa-linkedin-in'
    return 'fab fa-' + provider_id


@register.simple_tag(takes_context=True)
def animation_duration(context, duration=1000):
    request = context.get('request')
    if request.user_agent.is_mobile:
        return 0
    return duration


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
    icon_class = "fas fa-info-circle"
    bold_text = "Heads Up!"
    level_tag = message.level_tag
    if message.level == messages.SUCCESS:
        icon_class = "fas fa-check-circle"
        bold_text = "Success!"
    elif message.level == messages.WARNING:
        icon_class = "fas fa-exclamation-triangle"
        bold_text = "Warning!"
    elif message.level == messages.ERROR:
        icon_class = "fas fa-minus-circle"
        bold_text = "Uh-oh!"
        level_tag = "danger"
    return alert(level_tag, icon_class, bold_text, message.message, True)


@register.simple_tag(takes_context=True)
def mobile_friendly_image(context, image_path):
    """
    Returns the mobile image file path if the user agent is a mobile
    device; otherwise the original image file path.

    Note: if the image_path is 'img/myimg.jpg', there must also be 
          a file 'img/myimg.mobile.jpg'.
    """
    request = context.get('request')
    if not request.user_agent.is_mobile:
        return image_path
    split = os.path.splitext(image_path)
    return "{}.mobile{}".format(split[0], split[1])


@register.filter
def versioned_url(url):
    """ 
    Returns the url appended with a 'version=settings.VERSION' URL parameter

    This is primarily used for cache-busting.
    """
    return url + '?version=' + settings.VERSION if not '?' in url else url + '&version=' + settings.VERSION


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


@register.inclusion_tag('zinnia/tags/dummy.html')
def get_recent_category_entries(category_slug, number=5, template='zinnia/tags/entries_recent.html'):
    """
    Return the most recent entries for the specified category.
    """
    return {'template': template,
            'entries': Entry.published.filter(categories__slug=category_slug)[:number]}


@register.inclusion_tag("members/_profile_pic_thumbnail.html")
def profile_pic(member, size, className):
    """
    Given a member model, returns the HTML for a profile pic of that member.

    Parameters:
        member - the member model instance
        size - the required size of the picture (e.g. "200x200")
        className - the class to assign to the wrapper div
    """
    fallback_image = 'img/kit/ladies_shirt_sq.png' if (
        member and member.gender == Gender.Female) else 'img/kit/mens_shirt_sq.png'
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
    json_value = jsonlib.dumps(value)

    # Causes problems with jsonlib.loads below
    # clean = bleach.clean(json_value)

    # Minor hack to keep ampersands as they were
    # Note: Not needed now that we're not calling bleach.clean()
    # clean = clean.replace("&amp;", "&")

    try:
        jsonlib.loads(json_value)
    except:
        traceback.print_exc()
        # should never happen, but this is a last-line-of-defense check
        # to make sure this blob wont get eval'ed by the JS engine as
        # anything other than a JSON object
        raise ValueError(
            'JSON contains a quote or escape sequence that was unable to be stripped')

    return mark_safe(json_value)


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


@register.simple_tag
def clubinfo_email(key, linktext=None):
    """A simple tag that returns an obfuscated mailto: link to the email address matching
    the given key from the ClubInfo table."""
    return obfuscate(clubinfo(key), linktext)


clubinfo_email.needs_autoescape = True


@register.simple_tag(takes_context=True)
def active_link(context, viewname, *args, **kwargs):
    """
    Renders the 'active' CSS class if the request path matches the path of the view.
    :param context: The context where the tag was called. Used to access the request object.
    :param viewname: The name of the view (include namespaces if any).
    :return:
    """
    request = context.get('request')
    if request is None:
        # Can't work without the request object.
        return ''
    path = reverse(viewname, args=args, kwargs=kwargs)
    if request.path == path:
        return 'active'
    return ''


@register.inclusion_tag('comments/_recent.html')
def recent_comments(count=10):
    """ Utility for rendering the latest comments """
    comments = FluentComment.objects.filter(
        is_public=True, is_removed=False).order_by('-submit_date')[:count]
    return {
        'comments': comments,
    }

############################################################################################
# ADMIN INTERACE SUPPORT


@register.inclusion_tag('blocks/_admin_link.html', takes_context=True)
def instance_admin_links(context, model, change=True, add=False, changelist=False, change_url=None):
    """
    """
    try:
        content_type = ContentType.objects.get_for_model(model)
        return AdminLinksCreator(content_type.app_label, content_type.name, content_type.model, model.pk, change, add, changelist, change_url).render(context)
    except:
        LOG.error("Failed to render instance_admin_links", exc_info=True)


@register.inclusion_tag('blocks/_admin_link.html', takes_context=True)
def model_admin_links(context, app_label, model_name, add=True, changelist=True):
    """
    """
    try:
        content_type = ContentType.objects.get(
            app_label=app_label, model=model_name)
        return AdminLinksCreator(content_type.app_label, content_type.name, content_type.model, None, False, add, changelist).render(context)
    except:
        LOG.error("Failed to render model_admin_links", exc_info=True)


class AdminLinksCreator(object):

    def __init__(self, app_label, friendly_name, model_name, instance_id=None, change=False, add=False, changelist=False, change_url=None):
        self.app_label = app_label
        self.friendly_name = friendly_name
        self.model_name = model_name
        self.instance_id = instance_id
        self.change = change
        self.add = add
        self.changelist = changelist
        self.change_url = change_url

    def render(self, context):
        ctx = {}
        user = context['user']
        ctx['user'] = user
        should_display = False

        if self.change and self.has_perm(user, 'change_'):
            ctx['change_url'] = self.change_url if self.change_url else self.get_admin_change_url()
            ctx['change_label'] = "Edit " + self.friendly_name
            should_display = True
        else:
            ctx['change_url'] = None
            ctx['change_label'] = None

        if self.add and self.has_perm(user, 'add_'):
            ctx['add_url'] = self.get_admin_add_url()
            ctx['add_label'] = "Add " + self.friendly_name
            should_display = True
        else:
            ctx['add_url'] = None
            ctx['add_label'] = None

        if self.changelist and self.has_perm(user):
            ctx['list_url'] = self.get_admin_list_url()
            ctx['list_label'] = self.friendly_name.capitalize() + " list"
            should_display = True
        else:
            ctx['list_url'] = None
            ctx['list_label'] = None

        ctx['display_admin_links'] = should_display
        return ctx

    def get_admin_change_url(self):
        return reverse("admin:%s_%s_change" % (self.app_label, self.model_name), args=(self.instance_id,))

    def get_admin_add_url(self):
        return reverse("admin:%s_%s_add" % (self.app_label, self.model_name))

    def get_admin_list_url(self):
        return reverse("admin:%s_%s_changelist" % (self.app_label, self.model_name))

    def has_perm(self, user, prefix=''):
        return user.has_perm('{}.{}{}'.format(self.app_label, prefix, self.model_name))
