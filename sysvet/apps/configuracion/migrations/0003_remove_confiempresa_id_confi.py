# Generated by Django 3.1.5 on 2021-05-19 23:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configuracion', '0002_auto_20210517_2120'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='confiempresa',
            name='id_confi',
        ),
    ]
