# Generated by Django 3.1.5 on 2021-05-18 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0002_auto_20210517_2351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='stock_movido',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='tipoproducto',
            name='fecha_alta',
            field=models.CharField(default='17/05/2021 23:52:28 hs', editable=False, max_length=200),
        ),
    ]
