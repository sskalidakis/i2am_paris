# Generated by Django 2.2.5 on 2021-10-04 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('i2amparis_main', '0055_prweumetadata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prweumetadata',
            name='model_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='prweumetadata',
            name='region_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='prweumetadata',
            name='scenario_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='prweumetadata',
            name='variable_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='prwmetadata',
            name='model_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='prwmetadata',
            name='region_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='prwmetadata',
            name='scenario_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='prwmetadata',
            name='variable_name',
            field=models.CharField(default='', max_length=100),
        ),
    ]
