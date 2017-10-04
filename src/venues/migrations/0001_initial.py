# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-02 06:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=255, unique=True, verbose_name='Venue Name')),
                ('short_name', models.CharField(default=None, max_length=30, verbose_name='Short name')),
                ('slug', models.SlugField(verbose_name='Slug')),
                ('url', models.URLField(blank=True, verbose_name='Website')),
                ('is_home', models.BooleanField(default=False, verbose_name='Home ground')),
                ('phone', models.CharField(blank=True, max_length=20, verbose_name='Contact phone number')),
                ('addr1', models.CharField(blank=True, max_length=255, verbose_name='Address 1')),
                ('addr2', models.CharField(blank=True, max_length=255, verbose_name='Address 2')),
                ('addr3', models.CharField(blank=True, max_length=255, verbose_name='Address 3')),
                ('addr_city', models.CharField(blank=True, max_length=255, verbose_name='City')),
                ('addr_postcode', models.CharField(blank=True, max_length=10, verbose_name='Post Code')),
                ('notes', models.TextField(blank=True, verbose_name='Notes')),
                ('distance', models.PositiveSmallIntegerField(null=True, verbose_name='Distance to this venue')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]