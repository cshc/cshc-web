# Generated by Django 2.0.9 on 2020-10-16 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0020_auto_20200115_2044'),
    ]

    operations = [
        migrations.AddField(
            model_name='goalking',
            name='l7_goals',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Goals for Ladies 7ths'),
        ),
        migrations.AddField(
            model_name='goalking',
            name='l7_own_goals',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Own goals for Ladies 7ths'),
        ),
    ]
