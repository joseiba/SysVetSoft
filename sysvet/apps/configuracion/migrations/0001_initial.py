# Generated by Django 3.1.5 on 2021-04-26 02:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConfiEmpresa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semana', models.CharField(max_length=200)),
                ('apertura', models.CharField(max_length=200)),
                ('cierre', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Configuracion Empresa',
                'verbose_name_plural': 'Configuraciones Empresas',
            },
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod_serv', models.CharField(max_length=200)),
                ('nombre_servicio', models.CharField(help_text='Ingrese nombre del servicio', max_length=200)),
                ('precio_servicio', models.CharField(help_text='Ingrese el precio del servicio', max_length=200)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('is_active', models.CharField(blank=True, default='S', max_length=200, null=True)),
            ],
            options={
                'verbose_name': 'Servicio',
                'verbose_name_plural': 'Servicios',
            },
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_emp', models.CharField(max_length=200)),
                ('apellido_emp', models.CharField(max_length=200)),
                ('ci_empe', models.CharField(max_length=200)),
                ('disponible', models.BooleanField(blank=True, default=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('is_active', models.CharField(blank=True, default='S', max_length=200, null=True)),
                ('id_servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configuracion.servicio')),
            ],
            options={
                'verbose_name': 'Empleado',
                'verbose_name_plural': 'Empleados',
            },
        ),
    ]
