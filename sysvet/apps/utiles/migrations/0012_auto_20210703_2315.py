# Generated by Django 3.1.5 on 2021-07-04 03:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0012_auto_20210703_2315'),
        ('utiles', '0011_auto_20210626_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cedula',
            name='fecha_alta',
            field=models.CharField(blank=True, default='03/07/2021 23:15:03 hs', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='ruc',
            name='fecha_alta',
            field=models.CharField(blank=True, default='03/07/2021 23:15:03 hs', max_length=500, null=True),
        ),
        migrations.CreateModel(
            name='VacunasAplicadas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_aplicadas', models.FloatField(blank=True, default=0, null=True)),
                ('id_producto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='producto.producto')),
            ],
        ),
    ]
