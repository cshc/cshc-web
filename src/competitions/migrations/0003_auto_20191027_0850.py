# Generated by Django 2.0.9 on 2019-10-27 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competitions', '0002_auto_20171006_1844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='divisionresult',
            name='points',
            field=models.SmallIntegerField(default=0),
        ),
    ]