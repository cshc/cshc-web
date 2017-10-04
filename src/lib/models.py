""" Model utils """


# pylint: disable=C0103

class TeamGender(object):
    """ Enumeration of genders for teams """
    Mens = 'M'
    Ladies = 'L'
    Mixed = 'ML'
    Choices = (
        ('M', 'Mens'),
        ('L', 'Ladies'),
        ('ML', 'Mixed'),
    )


class TeamOrdinal(object):
    """ Enumeration of choices for a team's ordinal. Used in multiple apps. """
    T1 = '1sts'
    T2 = '2nds'
    T3 = '3rds'
    T4 = '4ths'
    T5 = '5ths'
    T6 = '6ths'
    T7 = '7ths'
    T8 = '8ths'
    T9 = '9ths'
    T10 = '10ths'
    T11 = '11ths'
    T12 = '12ths'
    TVets = 'Vets'
    TIndoor = 'Indoor'
    TOther = 'Other'
    Choices = (
        ('T1', '1sts'),
        ('T2', '2nds'),
        ('T3', '3rds'),
        ('T4', '4ths'),
        ('T5', '5ths'),
        ('T6', '6ths'),
        ('T7', '7ths'),
        ('T8', '8ths'),
        ('T9', '9ths'),
        ('T10', '10ths'),
        ('T11', '11ths'),
        ('T12', '12ths'),
        ('TVets', 'Vets'),
        ('TIndoor', 'Indoor'),
        ('TOther', 'Other'),
    )


def ordinal_from_TeamOrdinal(team_ordinal):
    """ Given a team ordinal, returns the actual ordinal part (stripping off the leading 'T')"""
    return team_ordinal.lstrip('T')
