from .models import Division, Season


def js_seasons():
    """
    Return a list of all seasons, suitable for passing to JavaScript
    """
    return list(Season.objects.order_by('-start').values_list('slug', flat=True))


def js_divisions(season=None):
    """
    Return a list of all divisions, with 'id', 'gender' and 'name' properties
    (suitable for passing to JavaScript)
    """
    divisions = Division.objects.select_related('league').only(
        'id', 'name', 'league__name', 'gender')
    if season is not None:
        divisions = divisions.filter(clubteamseasonparticipation__season=season).order_by(
            'clubteamseasonparticipation__team__position')

    return [{'id': x.id, 'gender': x.gender, 'name': "{} {}".format(
        x.league.name, x.name)} for x in divisions]
