# Generated by Django 3.0.7 on 2021-03-08 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('i2amparis_main', '0047_variablesres_agg_func'),
    ]

    operations = [
        migrations.AddField(
            model_name='regionsres',
            name='reg_type',
            field=models.IntegerField(default=0),
        ),
    ]