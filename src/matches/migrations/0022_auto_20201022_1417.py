# Generated by Django 2.0.9 on 2020-10-22 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0021_auto_20201016_0148'),
    ]

    operations = [
        migrations.AddField(
            model_name='goalking',
            name='mixedB_goals',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Goals for Mixed B team'),
        ),
        migrations.AddField(
            model_name='goalking',
            name='mixedB_own_goals',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Own goals for Mixed B team'),
        ),
    ]
