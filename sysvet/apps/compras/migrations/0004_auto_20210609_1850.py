# Generated by Django 3.1.5 on 2021-06-09 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0003_auto_20210609_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='fecha_alta',
            field=models.CharField(default='09/06/2021 18:50:52 hs', editable=False, max_length=200),
        ),
    ]
