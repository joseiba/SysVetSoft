# Generated by Django 3.1.5 on 2021-06-20 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0006_auto_20210619_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventario',
            name='fecha_alta',
            field=models.CharField(default='20/06/2021 12:26:27 hs', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='fecha_compra',
            field=models.CharField(default='20/06/2021', editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='tipoproducto',
            name='fecha_alta',
            field=models.CharField(default='20/06/2021 12:26:27 hs', editable=False, max_length=200),
        ),
    ]
