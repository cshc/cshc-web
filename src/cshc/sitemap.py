"""
    This module defines the sitemaps for ALL apps in the CSHC website.
    Ref: https://docs.djangoproject.com/en/1.11/ref/contrib/sitemaps/

    The sitemap is split into sections, each of which is referenced by
    the sitemap index. See definition of 'CshcSitemap' below for details.
"""

from django.contrib.sitemaps import Sitemap
from django.contrib.flatpages.sitemaps import FlatPageSitemap
from django.urls import reverse
from zinnia.sitemaps import TagSitemap
from zinnia.sitemaps import EntrySitemap
from zinnia.sitemaps import CategorySitemap
from zinnia.sitemaps import AuthorSitemap
from matches.sitemaps import MatchesSitemap
from members.sitemaps import MembersSitemap
from opposition.sitemaps import OppositionSitemap
from teams.sitemaps import ClubTeamSitemap
from training.sitemaps import TrainingSitemap
from venues.sitemaps import VenuesSitemap
from competitions.sitemaps import SeasonalSitemap
from competitions.models import Season


class MainStaticViewSitemap(Sitemap):
    """ High-priority static pages. """
    priority = 1.0
    changefreq = 'monthly'

    def items(self):
        return [
            'homepage', 'about_us', 'directions', 'about_kit', 'member_offers',
            'calendar', 'join_us', 'about_committee', 'juniors_index', 'contact_us',
            'stats',
        ]

    def location(self, obj):
        return reverse(obj)


class ArchiveStaticViewSitemap(Sitemap):
    """ Low priority (archive) static pages. """
    priority = 0.6
    changefreq = 'never'

    def items(self):
        return [
            'about_minutes',
        ]

    def location(self, obj):
        return reverse(obj)


class CommitteeSitemap(SeasonalSitemap):
    """ Sitemap of committee pages through the years. """

    def priority(self, item):
        if item == Season.current():
            return 1.0
        else:
            return 0.7

    def changefreq(self, item):
        if item == Season.current():
            return 'monthly'
        else:
            return 'yearly'

    def url_name(self):
        return 'about_committee_season'


# Dictionary of sitemap sections to Sitemap classes
# Note: We're using an index so each sitemap section can be
# found at /sitemap-<section>.xml
CshcSitemap = {
    **MatchesSitemap,
    **MembersSitemap,
    **OppositionSitemap,
    **ClubTeamSitemap,
    **TrainingSitemap,
    ** VenuesSitemap,
    'flatpages': FlatPageSitemap,
    'main': MainStaticViewSitemap,
    'archive': ArchiveStaticViewSitemap,
    'committee': CommitteeSitemap,

    # Zinnia Blog - ref: http://django-blog-zinnia.readthedocs.org/en/latest/getting-started/configuration.html#module-zinnia.sitemaps
    'tags': TagSitemap,
    'blog': EntrySitemap,
    'authors': AuthorSitemap,
    'categories': CategorySitemap,
}
