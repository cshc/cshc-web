# Generated by Django 2.0.1 on 2018-07-12 11:00

from django.db import migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0007_auto_20180710_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clubteamseasonparticipation',
            name='team_photo_cropping',
            field=image_cropping.fields.ImageRatioField('team_photo', '1200x800', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=False, verbose_name='team photo cropping'),
        ),
    ]