from django.db import migrations, models
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0016_auto_20190729_1618'),
    ]

    operations = [
        migrations.RenameField('goalking', 'indoor_goals', 'mind_goals'),
        migrations.RenameField('goalking', 'indoor_own_goals', 'mind_own_goals'),
    ]
