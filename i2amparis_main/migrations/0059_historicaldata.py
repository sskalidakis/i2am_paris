# Generated by Django 2.2.5 on 2021-11-19 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('i2amparis_main', '0058_euharmdata'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('value', models.FloatField()),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='i2amparis_main.UnitsRes')),
                ('variable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='i2amparis_main.VariablesRes')),
            ],
        ),
    ]
