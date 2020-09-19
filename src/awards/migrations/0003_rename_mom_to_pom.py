import traceback
from django.db import migrations

def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    MatchAward = apps.get_model("awards", "matchaward")
    db_alias = schema_editor.connection.alias
    manager = MatchAward.objects.using(db_alias)

    # Rename 'Man of the Match' to 'Player of the Match'
    try:
        mom = manager.get(name='Man of the Match')
        mom.name = 'Player of the Match'
        mom.save()
    except MatchAward.DoesNotExist:
        print('Man of the Match award not found - skipping migration action')
        pass

def reverse_func(apps, schema_editor):
    # Reverse the changes that forwards_func() makes
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    MatchAward = apps.get_model("awards", "matchaward")
    db_alias = schema_editor.connection.alias
    manager = MatchAward.objects.using(db_alias)

    # Rename 'Player of the Match' to 'Man of the Match'
    try:
        mom = manager.get(name='Player of the Match')
        mom.name = 'Man of the Match'
        mom.save()
    except MatchAward.DoesNotExist:
        print('Player of the Match award not found - skipping migration action')
        pass

class Migration(migrations.Migration):

    dependencies = [
        ('awards', '0002_auto_20180117_1040'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
