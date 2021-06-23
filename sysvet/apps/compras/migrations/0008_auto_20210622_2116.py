# Generated by Django 3.1.5 on 2021-06-23 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0007_auto_20210619_2023'),
    ]

    operations = [
        migrations.AddField(
            model_name='facturadet',
            name='precio_compra',
            field=models.CharField(blank=True, max_length=800, null=True),
        ),
        migrations.AlterField(
            model_name='facturacompra',
            name='fecha_alta',
            field=models.CharField(default='22/06/2021', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='fecha_alta',
            field=models.CharField(default='22/06/2021 21:16:45 hs', editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='pedidocabecera',
            name='fecha_alta',
            field=models.CharField(default='22/06/2021', editable=False, max_length=200),
        ),
    ]
