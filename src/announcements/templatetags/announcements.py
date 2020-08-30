""" Template tags for Announcements """

from django.template import Library
from announcements.models import Announcement, AnnouncementStyle

register = Library()

def getAttribs(announcement):
    color = 'g-bg-gray-dark-v2 g-color-white'
    icon = 'icon-info'
    if announcement['style'] == AnnouncementStyle.Danger:
        color = 'g-bg-red g-color-white'
        icon = 'icon-ban'
    elif announcement['style'] == AnnouncementStyle.Warning:
        color = 'g-bg-yellow'
        icon = 'icon-exclamation'
    elif announcement['style'] == AnnouncementStyle.Success:
        color = 'g-bg-teal g-color-white'
        icon = 'icon-check'
    return { 'color': color, 'icon': icon }

@register.inclusion_tag('announcements/dummy.html')
def list_announcements(template):
    """
    Return all active announcements.
    """
    announcements = [ {
        'title': a.title,
        'content': a.content,
        'style': a.style
    } for a in Announcement.objects.active()]
    for a in announcements:
        a.update(getAttribs(a))
    return {'template': template,
            'announcements': announcements}
