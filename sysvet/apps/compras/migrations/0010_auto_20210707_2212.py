# Generated by Django 3.1.5 on 2021-07-08 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0009_auto_20210707_2157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='fecha_alta',
            field=models.CharField(default='07/07/2021 22:12:14 hs', editable=False, max_length=200),
        ),
    ]
