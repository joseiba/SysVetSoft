# Generated by Django 3.1.5 on 2021-06-03 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0011_auto_20210529_0050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='fecha_alta',
            field=models.CharField(default='02/06/2021 21:07:57 hs', editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='pedidocabecera',
            name='fecha_alta',
            field=models.CharField(default='02/06/2021', editable=False, max_length=200),
        ),
    ]
