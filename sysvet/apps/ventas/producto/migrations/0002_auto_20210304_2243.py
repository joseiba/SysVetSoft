# Generated by Django 3.1.5 on 2021-03-05 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tipoproducto',
            name='fecha_alta',
            field=models.CharField(default='04/03/2021 22:43:32 hs', editable=False, max_length=200),
        ),
    ]