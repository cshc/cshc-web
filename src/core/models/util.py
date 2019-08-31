""" Model utils """

import uuid
from django.core.exceptions import ObjectDoesNotExist
from model_utils import Choices


def get_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except ObjectDoesNotExist:
        return None

# pylint: disable=C0103


def make_unique_filename(filename):
    """ Produces a unique filename, combining the given filename
        and a uuid.
    """
    return "%s-%s" % (uuid.uuid4(), filename)


class DivisionResult(object):
    """ Enumeration of division results """
    Promoted = 'Promoted'
    Relegated = 'Relegated'
    Champions = 'Champions'
    Choices = [
        ('Promoted', 'Promoted'),
        ('Relegated', 'Relegated'),
        ('Champions', 'Champions'),
    ]


class TeamGender(object):
    """ Enumeration of genders for teams """
    Mens = 'Mens'
    Ladies = 'Ladies'
    Mixed = 'Mixed'
    Choices = (
        ('Mens', 'Mens'),
        ('Ladies', 'Ladies'),
        ('Mixed', 'Mixed'),
    )


# Enumeration of choices for a team's ordinal. Used in multiple apps.
TeamOrdinal = Choices(
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
    ('TMVets', "Men's Vets"),
    ('TLVets', "Ladies' Vets"),
    ('TMIndoor', "Men's Indoor"),
    ('TLIndoor', "Ladies' Indoor"),
    ('TOther', 'Other')
)


class Gender(object):
    """ Enumeration of choices for member's gender """
    Male = 'Male'
    Female = 'Female'
    Choices = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )


class Position(object):
    """ Enumeration of preferred positions """
    GK = 0
    GK_Def = 1
    GK_Mid = 2
    GK_Fwd = 3
    Def = 4
    Def_Mid = 5
    Mid = 6
    Mid_Fwd = 7
    Fwd = 8
    Other = 9
    Choices = (
        (0, 'Goalkeeper'),
        (1, 'Goalkeeper/Defender'),
        (2, 'Goalkeeper/Midfielder'),
        (3, 'Goalkeeper/Forward'),
        (4, 'Defender'),
        (5, 'Defender/Midfielder'),
        (6, 'Midfielder'),
        (7, 'Midfielder/Forward'),
        (8, 'Forward'),
        (9, 'Not known'))


EmergencyContactRelationship = Choices(
    'Spouse', 'Partner', 'Parent', 'Sibling', 'Friend', 'Other')


def ordinal_from_TeamOrdinal(team_ordinal):
    """ Given a team ordinal, returns the actual ordinal part (stripping off the leading 'T')"""
    return team_ordinal.lstrip('T')
