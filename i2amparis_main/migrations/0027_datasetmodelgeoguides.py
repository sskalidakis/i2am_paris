# Generated by Django 2.2.5 on 2020-09-10 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('i2amparis_main', '0026_auto_20200731_1438'),
    ]

    operations = [
        migrations.CreateModel(
            name='DatasetModelGeoGuides',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guide_from', models.CharField(default='', max_length=50)),
                ('guide_to', models.CharField(default='', max_length=50)),
                ('value', models.CharField(default='', max_length=50)),
            ],
        ),
    ]
