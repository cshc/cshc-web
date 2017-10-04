# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-04 06:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateField(help_text='(Approx) first day of the season', verbose_name='Season start')),
                ('end', models.DateField(help_text='(Approx) last day of the season', verbose_name='Season end')),
                ('slug', models.SlugField()),
            ],
            options={
                'ordering': ['start'],
                'get_latest_by': 'start',
            },
        ),
    ]