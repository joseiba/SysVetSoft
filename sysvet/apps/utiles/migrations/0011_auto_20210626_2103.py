# Generated by Django 3.1.5 on 2021-06-27 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utiles', '0010_auto_20210626_1825'),
    ]

    operations = [
        migrations.AddField(
            model_name='productocompradomes',
            name='anho',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='productovendidomes',
            name='anho',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='cedula',
            name='fecha_alta',
            field=models.CharField(blank=True, default='26/06/2021 21:03:29 hs', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='ruc',
            name='fecha_alta',
            field=models.CharField(blank=True, default='26/06/2021 21:03:29 hs', max_length=500, null=True),
        ),
    ]
