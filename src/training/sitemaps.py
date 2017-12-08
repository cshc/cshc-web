"""
  Sitemaps for training URLs
"""

from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse
from .models import TrainingSession


class UpcomingTrainingSessionsSitemap(Sitemap):
    """ Sitemap for the upcoming training sessions page. """
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return ['upcoming_trainingsession_list']

    def location(self, obj):
        return reverse(obj)


class TrainingDetailSitemap(Sitemap):
    """ Sitemap of all the training session details pages. """
    priority = 0.4
    changefreq = 'weekly'

    def items(self):
        return TrainingSession.objects.all()


TrainingSitemap = {
    'upcoming-training': UpcomingTrainingSessionsSitemap,
    'training-detail': TrainingDetailSitemap,
}
