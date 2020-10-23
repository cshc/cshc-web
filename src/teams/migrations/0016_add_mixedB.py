import traceback
from django.db import migrations
import image_cropping.fields
from core.models import TeamGender, TeamOrdinal

def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    Season = apps.get_model("competitions", "season")
    ClubTeam = apps.get_model("teams", "clubteam")
    ClubTeamSeasonParticipation = apps.get_model("teams", "clubteamseasonparticipation")
    
    db_alias = schema_editor.connection.alias
    
    manager = ClubTeam.objects.using(db_alias)
    part_manager = ClubTeamSeasonParticipation.objects.using(db_alias)
    season_manager = Season.objects.using(db_alias)
    
    # Add Mixed B team
    mixedB = manager.create(
        short_name='Mixed-B',
        long_name="Mixed B XI",
        gender=TeamGender.Mixed,
        ordinal=TeamOrdinal.TOther,
        position=62,
        southerners=True,
        rivals=True,
        fill_blanks=False,
        personal_stats=True,
        active=True,
        slug='mixed-b',
    )
    current_season = season_manager.get(slug='2020-2021')
    part_manager.create(team=mixedB, season=current_season)


def reverse_func(apps, schema_editor):
    # Reverse the changes that forwards_func() makes
    # Do nothing
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0015_add_l7'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
