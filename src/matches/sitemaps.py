"""
  Sitemaps for match URLs.abs

  Currently no sitemaps are generated for feed URLs
"""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from competitions.sitemaps import SeasonalSitemap
from .models import Match


class MatchStatsSitemap(Sitemap):
    """ Sitemap of pages that list matches or match-related stats. """
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return ['match_list', 'goal_king', 'accidental_tourist', 'naughty_step']

    def location(self, obj):
        return reverse(obj)


class AccidentalTouristSeasonSitemap(SeasonalSitemap):
    """ Sitemap of the accidental tourist pages for each season. """
    priority = 0.5
    changefreq = 'weekly'

    def url_name(self):
        return 'accidental_tourist_season'


class NaughtyStepSitemap(SeasonalSitemap):
    """ Sitemap of the naughty step pages for each season. """
    priority = 0.5
    changefreq = 'weekly'

    def url_name(self):
        return 'naughty_step_season'


class MatchDetailSitemap(Sitemap):
    """ Sitemap of each match details page. """
    priority = 0.5
    changefreq = "weekly"

    def items(self):
        return Match.objects.all()

    def lastmod(self, obj):
        return obj.report_pub_timestamp


MatchesSitemap = {
    'match-stats': MatchStatsSitemap,
    'accidental-tourist-season': AccidentalTouristSeasonSitemap,
    'naughty-step-season': NaughtyStepSitemap,
    'match-detail': MatchDetailSitemap,
}
