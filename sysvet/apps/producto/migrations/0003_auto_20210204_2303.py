# Generated by Django 3.1.5 on 2021-02-05 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0002_auto_20210204_2300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tipoproducto',
            name='fecha_baja',
            field=models.DateTimeField(blank=True, default='00/00/0000 00:00:00', null=True),
        ),
    ]
