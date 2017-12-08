"""
  Sitemaps for team URLs
"""

from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse
from competitions.sitemaps import SeasonalSitemap
from competitions.models import Season
from .models import ClubTeam


class ClubTeamListSitemap(Sitemap):
    """ Sitemap of the club team list page. """
    priority = 0.5
    changefreq = 'yearly'

    def items(self):
        return ['clubteam_list']

    def location(self, obj):
        return reverse(obj)


class ClubTeamStatsSitemap(Sitemap):
    """ Sitemap of pages that relate to club team stats. """
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return ['southerners_league', 'playing_record']

    def location(self, obj):
        return reverse(obj)


class SouthernersLeagueSeasonSitemap(SeasonalSitemap):
    """ Sitemap of the accidental tourist pages for each season. """
    priority = 0.5
    changefreq = 'weekly'

    def url_name(self):
        return 'southerners_league_season'


class ClubTeamDetailSitemap(Sitemap):
    """ Sitemap of all the club team's details pages (default view)"""
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return ClubTeam.objects.all()


class ClubTeamArchiveSitemap(Sitemap):
    """ Sitemap of all the club team's details pages for all seasons. """
    priority = 0.5
    changefreq = 'yearly'

    def items(self):
        teams = ClubTeam.objects.all()
        items = []
        for team in teams:
            seasons = Season.objects.filter(
                clubteamseasonparticipation__team=team)
            for season in seasons:
                items.append((team.slug, season.slug))
        return items

    def location(self, obj):
        return reverse('clubteam_season_detail', args=[obj[0], obj[1]])


ClubTeamSitemap = {
    'clubteam-list': ClubTeamListSitemap,
    'clubteam-stats': ClubTeamStatsSitemap,
    'southerners-league-season': SouthernersLeagueSeasonSitemap,
    'clubteam-detail': ClubTeamDetailSitemap,
    'clubteam-detail-season': ClubTeamArchiveSitemap,
}
