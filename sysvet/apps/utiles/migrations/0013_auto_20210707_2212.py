# Generated by Django 3.1.5 on 2021-07-08 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utiles', '0012_auto_20210703_2315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cedula',
            name='fecha_alta',
            field=models.CharField(blank=True, default='07/07/2021 22:12:14 hs', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='ruc',
            name='fecha_alta',
            field=models.CharField(blank=True, default='07/07/2021 22:12:14 hs', max_length=500, null=True),
        ),
    ]
