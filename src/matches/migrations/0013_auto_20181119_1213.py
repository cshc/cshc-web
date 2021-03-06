# Generated by Django 2.0.9 on 2018-11-19 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0012_auto_20181119_1157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appearance',
            name='green_card_count',
            field=models.PositiveSmallIntegerField(blank=True, default=0, help_text='The number of green cards the player received in the match', null=True),
        ),
        migrations.AlterField(
            model_name='appearance',
            name='yellow_card_count',
            field=models.PositiveSmallIntegerField(blank=True, default=0, help_text='The number of yellow cards the player received in the match', null=True),
        ),
    ]
