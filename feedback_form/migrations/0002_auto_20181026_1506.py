# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-26 12:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback_form', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedback',
            name='email',
        ),
        migrations.RemoveField(
            model_name='feedback',
            name='happy',
        ),
        migrations.RemoveField(
            model_name='feedback',
            name='product',
        ),
        migrations.AddField(
            model_name='feedback',
            name='rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='feedback',
            name='service',
            field=models.CharField(default='', max_length=120),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='details',
            field=models.TextField(default=''),
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]
