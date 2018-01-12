"""
  Re-usable sitemap utilities relating to competitions - primarily seasons 
"""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Season


class SeasonalSitemap(Sitemap):
    """ Utility abstract sitemap class.

        Derived classes must provide a url_name method.
    """
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return Season.objects.all()

    def location(self, item):
        return reverse(self.url_name(), args=[item.slug])
