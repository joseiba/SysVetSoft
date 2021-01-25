# Generated by Django 3.1.5 on 2021-01-21 03:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ciudad',
            fields=[
                ('id_ciudad', models.IntegerField(help_text='Código para la ciudad', primary_key=True, serialize=False)),
                ('nombre_ciudad', models.CharField(help_text='Ingrese nombre de la ciudad', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id_cliente', models.IntegerField(help_text='Código para el cliente', primary_key=True, serialize=False)),
                ('nombre_cliente', models.CharField(help_text='Ingrese nombre del cliente', max_length=200)),
                ('apellido_cliente', models.CharField(help_text='Ingrese apellido del cliente', max_length=200)),
                ('direccion', models.CharField(help_text='Ingrese apellido del cliente', max_length=200)),
                ('cedula', models.CharField(help_text='Ingrese cedula del cliente', max_length=200)),
                ('ruc', models.CharField(help_text='Ingrese ruc del cliente', max_length=200)),
                ('telefono', models.CharField(help_text='Ingrese telefono del cliente', max_length=200)),
                ('email', models.CharField(help_text='Ingrese email del cliente', max_length=200)),
                ('id_ciudad', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cliente.ciudad')),
            ],
        ),
    ]
