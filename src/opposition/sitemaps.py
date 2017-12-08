"""
  Sitemaps for opposition URLs.abs
"""

from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse
from .models import Club


class OppositionClubListSitemap(Sitemap):
    """ Sitemap of the oppositions club list page. """
    priority = 0.3
    changefreq = 'monthly'

    def items(self):
        return ['opposition_club_list']

    def location(self, obj):
        return reverse(obj)


class OppositionClubDetailSitemap(Sitemap):
    """ Sitemap of each opposition club details page. """
    priority = 0.3
    changefreq = "monthly"

    def items(self):
        return Club.objects.all()


OppositionSitemap = {
    'oppositionclub-list': OppositionClubListSitemap,
    'oppositionclub-detail': OppositionClubDetailSitemap,
}
