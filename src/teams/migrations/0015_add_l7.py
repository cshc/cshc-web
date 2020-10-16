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
    
    # Add L7 team
    l7 = manager.create(
        short_name='L7',
        long_name="Ladies' 7th XI",
        gender=TeamGender.Ladies,
        ordinal=TeamOrdinal.T7,
        position=18,
        southerners=True,
        rivals=True,
        fill_blanks=False,
        personal_stats=True,
        active=True,
        slug='l7',
    )
    current_season = season_manager.get(slug='2020-2021')
    part_manager.create(team=l7, season=current_season)


def reverse_func(apps, schema_editor):
    # Reverse the changes that forwards_func() makes
    # Do nothing
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0014_add_l6'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
