# Generated by Django 2.2.5 on 2019-11-17 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('i2amparis_main', '0002_modelsinfo_ordering'),
    ]

    operations = [
        migrations.AddField(
            model_name='modelsinfo',
            name='coverage',
            field=models.TextField(default=''),
        ),
    ]
