# Generated by Django 3.1.5 on 2021-06-17 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('factura', '0002_auto_20210615_2108'),
    ]

    operations = [
        migrations.AddField(
            model_name='facturacabeceraventa',
            name='factura_to_reporte',
            field=models.CharField(blank=True, default='N', max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='facturacabeceraventa',
            name='fecha_alta',
            field=models.CharField(default='16/06/2021', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='facturacabeceraventa',
            name='fecha_emision',
            field=models.CharField(default='16/06/2021 20:24:52 hs', max_length=500, null=True),
        ),
    ]