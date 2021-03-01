# Generated by Django 2.1 on 2021-03-01 01:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mascota', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='especie',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='mascota',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='raza',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]