# Generated by Django 3.1.5 on 2021-03-05 02:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mascota', '0002_auto_20210304_2235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='especie',
            name='last_modified',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 4, 22, 41, 58, 104010)),
        ),
        migrations.AlterField(
            model_name='mascota',
            name='last_modified',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 4, 22, 41, 58, 105025)),
        ),
        migrations.AlterField(
            model_name='raza',
            name='last_modified',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 4, 22, 41, 58, 105025)),
        ),
    ]
