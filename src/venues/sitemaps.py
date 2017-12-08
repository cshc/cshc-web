"""
  Sitemaps for venue URLs
"""

from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse
from .models import Venue


class VenueListSitemap(Sitemap):
    """ Sitemap of the venues list page. """
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['venue_list']

    def location(self, obj):
        return reverse(obj)


class VenueDetailSitemap(Sitemap):
    """ Sitemap of each venue details page. """
    priority = 0.5
    changefreq = "monthly"

    def items(self):
        return Venue.objects.all()


VenuesSitemap = {
    'venue-list': VenueListSitemap,
    'venue-detail': VenueDetailSitemap,
}
