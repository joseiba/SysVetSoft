# Generated by Django 3.1.5 on 2021-06-24 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuracion', '0004_tipovacuna_multi_aplicaciones'),
    ]

    operations = [
        migrations.AddField(
            model_name='confiempresa',
            name='dias_alert_vacunas',
            field=models.IntegerField(blank=True, default=30, null=True),
        ),
    ]
