# Generated by Django 3.1.5 on 2021-06-09 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0004_auto_20210609_1850'),
    ]

    operations = [
        migrations.AddField(
            model_name='facturacompra',
            name='factura_caja',
            field=models.CharField(blank=True, default='N', max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='fecha_alta',
            field=models.CharField(default='09/06/2021 18:54:24 hs', editable=False, max_length=200),
        ),
    ]
