# Generated by Django 3.1.5 on 2021-07-08 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caja', '0003_auto_20210616_2301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caja',
            name='fecha_alta',
            field=models.CharField(default='07/07/2021', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='caja',
            name='fecha_hora_alta',
            field=models.CharField(default='07/07/2021 21:37:34 hs', max_length=500, null=True),
        ),
    ]