# Generated by Django 3.1.5 on 2021-06-17 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0005_auto_20210615_2326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facturacompra',
            name='fecha_alta',
            field=models.CharField(default='16/06/2021', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='fecha_alta',
            field=models.CharField(default='16/06/2021 20:25:04 hs', editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='pedidocabecera',
            name='fecha_alta',
            field=models.CharField(default='16/06/2021', editable=False, max_length=200),
        ),
    ]