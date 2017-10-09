""" Django views that don't fit nicely into one of the other apps.
"""

from django.views.generic import TemplateView


class HomeView(TemplateView):
    """ The main home page of the Cambridge South Hockey Club website. """
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        return context
