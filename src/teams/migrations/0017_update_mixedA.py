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
    
    # Update Mixed A team
    mixedA = manager.get(short_name='Mixed')
    mixedA.short_name = 'Mixed-A'
    mixedA.slug = 'mixed-a'
    mixedA.long_name = 'Mixed A XI'
    mixedA.save()
    

def reverse_func(apps, schema_editor):
    # Reverse the changes that forwards_func() makes
    # Do nothing
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0016_add_mixedB'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
