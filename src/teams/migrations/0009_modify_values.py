import traceback
from django.db import migrations
import image_cropping.fields
from core.models import TeamOrdinal

def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    ClubTeam = apps.get_model("teams", "clubteam")
    db_alias = schema_editor.connection.alias
    manager = ClubTeam.objects.using(db_alias)

    # Change the position of the Mixed team
    mixed = manager.get(short_name='Mixed')
    mixed.position = 15
    mixed.save()

    # Change the short_name, ordinal and slug of the Men's Indoor Team
    mind = manager.get(short_name='Indoor')
    mind.short_name = 'MInd'
    mind.ordinal = TeamOrdinal.TMIndoor
    mind.slug = 'mind'
    mind.save()
    
    # Change the ordinal of the Men's Vets Team
    mv = manager.get(short_name='MV')
    mv.ordinal = TeamOrdinal.TMVets
    mv.save()


def reverse_func(apps, schema_editor):
    # Reverse the changes that forwards_func() makes
    ClubTeam = apps.get_model("teams", "clubteam")
    db_alias = schema_editor.connection.alias
    manager = ClubTeam.objects.using(db_alias)

    # Change the short_name, ordinal and slug of the Men's Indoor Team
    mind = manager.get(short_name='MInd')
    mind.short_name = 'Indoor'
    mind.ordinal = 'TIndoor'
    mind.slug = 'indoor'
    mind.save()
    
    # Change the position of the Mixed team
    mixed = manager.get(short_name='Mixed')
    mixed.position = 12
    mixed.save()
    
    # Change the ordinal of the Men's Vets Team
    mv = manager.get(short_name='MV')
    mv.ordinal = 'TVets'
    mv.save()

class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0008_auto_20180712_1800'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
