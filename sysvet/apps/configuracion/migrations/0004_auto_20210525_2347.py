# Generated by Django 3.1.5 on 2021-05-26 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuracion', '0003_remove_confiempresa_id_confi'),
    ]

    operations = [
        migrations.AddField(
            model_name='confiempresa',
            name='cuidad',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='confiempresa',
            name='direccion',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='confiempresa',
            name='fecha_fin_timbrado',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='confiempresa',
            name='fecha_inicio_timbrado',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='confiempresa',
            name='nombre_empresa',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='confiempresa',
            name='nro_timbrado',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='confiempresa',
            name='telefono',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='confiempresa',
            name='apertura_caja_inicial',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='confiempresa',
            name='ubicacion_deposito_inicial',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
