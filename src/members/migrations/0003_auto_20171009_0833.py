# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-09 01:33
from __future__ import unicode_literals

from django.db import migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_auto_20171007_1455'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='cropping',
        ),
        migrations.AddField(
            model_name='member',
            name='profile_pic_cropping',
            field=image_cropping.fields.ImageRatioField('profile_pic', '400x400', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=False, verbose_name='profile pic cropping'),
        ),
    ]
