# Generated by Django 3.0.7 on 2020-10-20 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('i2amparis_main', '0038_auto_20201020_1713'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='regionsres',
            name='region',
        ),
        migrations.RemoveField(
            model_name='unitsres',
            name='unit',
        ),
        migrations.RemoveField(
            model_name='variablesres',
            name='variable',
        ),
    ]
