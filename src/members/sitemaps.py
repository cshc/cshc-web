"""
  Sitemaps for member URLs
"""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Member


class MemberListSitemap(Sitemap):
    """ Sitemap of the members list page. """
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return ['member_list']

    def location(self, obj):
        return reverse(obj)


class MemberDetailSitemap(Sitemap):
    """ Sitemap of each member details page. """
    priority = 0.5
    changefreq = "weekly"

    def items(self):
        return Member.objects.all()


MembersSitemap = {
    'member-list': MemberListSitemap,
    'member-detail': MemberDetailSitemap,
}
