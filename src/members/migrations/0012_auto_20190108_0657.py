# Generated by Django 2.0.9 on 2019-01-07 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0011_auto_20180220_1035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='emergency_phone',
            field=models.CharField(blank=True, help_text='Phone number of person to contact in an emergency', max_length=20, null=True, verbose_name='Emergency contact phone'),
        ),
        migrations.AlterField(
            model_name='member',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone number'),
        ),
    ]