import traceback
from django.db import migrations
import image_cropping.fields
from core.models import TeamGender, TeamOrdinal


def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    ClubTeam = apps.get_model("teams", "clubteam")

    db_alias = schema_editor.connection.alias

    manager = ClubTeam.objects.using(db_alias)

    # Update the Mens Indoor and Ladies Indoor team details
    try:
        mens_indoor = manager.get(slug='mind')
        mens_indoor.short_name = 'M-In'
        mens_indoor.slug = 'm-in'
        mens_indoor.save()
    except ClubTeam.DoesNotExist:
        print('Mens Indoor team not found')

    try:
        ladies_indoor = manager.get(slug='lind')
        ladies_indoor.short_name = 'L-In'
        ladies_indoor.slug = 'l-in'
        ladies_indoor.save()
    except ClubTeam.DoesNotExist:
        print('Ladies Indoor team not found')


def reverse_func(apps, schema_editor):
    # Reverse the changes that forwards_func() makes
    # Do nothing
    ClubTeam = apps.get_model("teams", "clubteam")

    db_alias = schema_editor.connection.alias

    manager = ClubTeam.objects.using(db_alias)

    # Revert the Mens Indoor and Ladies Indoor team details
    try:
        mens_indoor = manager.get(slug='m-in')
        mens_indoor.short_name = 'MInd'
        mens_indoor.slug = 'mind'
        mens_indoor.save()
    except ClubTeam.DoesNotExist:
        print('Mens Indoor team not found')

    try:
        ladies_indoor = manager.get(slug='l-in')
        ladies_indoor.short_name = 'LInd'
        ladies_indoor.slug = 'lind'
        ladies_indoor.save()
    except ClubTeam.DoesNotExist:
        print('Ladies Indoor team not found')


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0012_add_m6'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
