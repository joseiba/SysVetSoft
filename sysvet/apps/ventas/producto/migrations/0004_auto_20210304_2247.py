# Generated by Django 3.1.5 on 2021-03-05 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0003_auto_20210304_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tipoproducto',
            name='fecha_alta',
            field=models.CharField(default='04/03/2021 22:47:17 hs', editable=False, max_length=200),
        ),
    ]
