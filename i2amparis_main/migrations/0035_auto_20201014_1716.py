# Generated by Django 2.2.5 on 2020-10-14 14:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('i2amparis_main', '0034_datasetondemandvariableharmonisation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datasetondemandvariableharmonisation',
            name='var_source_info',
        ),
        migrations.RemoveField(
            model_name='datasetondemandvariableharmonisation',
            name='var_timespan',
        ),
        migrations.RemoveField(
            model_name='datasetondemandvariableharmonisation',
            name='var_unit',
        ),
    ]
