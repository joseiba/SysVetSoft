# Generated by Django 3.1.5 on 2021-06-10 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='fecha_compra',
            field=models.CharField(default='09/06/2021', editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='tipoproducto',
            name='fecha_alta',
            field=models.CharField(default='09/06/2021 21:14:48 hs', editable=False, max_length=200),
        ),
    ]