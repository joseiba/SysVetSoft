# Generated by Django 3.1.5 on 2021-06-10 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0004_auto_20210609_2119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tipoproducto',
            name='fecha_alta',
            field=models.CharField(default='09/06/2021 21:20:17 hs', editable=False, max_length=200),
        ),
    ]