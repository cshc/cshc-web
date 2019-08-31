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
    
    # Add Ladies Indoor and Vets teams
    lind = manager.create(
        short_name='LInd',
        long_name="Ladies' Indoor Team",
        gender=TeamGender.Ladies,
        ordinal=TeamOrdinal.TLInd,
        position=14,
        southerners=True,
        rivals=True,
        fill_blanks=False,
        personal_stats=True,
        active=True,
        slug='lind',
    )
    lv = manager.create(
        short_name='LV',
        long_name="Ladies' Veterans XI",
        gender=TeamGender.Ladies,
        ordinal=TeamOrdinal.TLVets,
        position=12,
        southerners=True,
        rivals=True,
        fill_blanks=False,
        personal_stats=True,
        active=True,
        slug='lv',
    )
    current_season = season_manager.get(slug='2019-2020')
    part_manager.create(team=lind, season=current_season)
    part_manager.create(team=lv, season=current_season)


def reverse_func(apps, schema_editor):
    # Reverse the changes that forwards_func() makes
    # Do nothing
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0009_modify_values'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
