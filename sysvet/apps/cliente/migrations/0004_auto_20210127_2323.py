# Generated by Django 2.1 on 2021-01-28 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0003_auto_20210127_2319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='email',
            field=models.EmailField(blank=True, default='', help_text='Ingrese email del cliente', max_length=200, null=True),
        ),
    ]
