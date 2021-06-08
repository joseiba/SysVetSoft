# Generated by Django 3.1.5 on 2021-06-05 21:57

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
                ('apertura_caja_inicial', models.CharField(blank=True, max_length=200, null=True)),
                ('ubicacion_deposito_inicial', models.CharField(blank=True, max_length=200, null=True)),
                ('nombre_empresa', models.CharField(blank=True, max_length=500, null=True)),
                ('direccion', models.CharField(blank=True, max_length=500, null=True)),
                ('cuidad', models.CharField(blank=True, max_length=500, null=True)),
                ('telefono', models.CharField(blank=True, max_length=500, null=True)),
                ('nro_timbrado', models.CharField(blank=True, max_length=500, null=True)),
                ('fecha_inicio_timbrado', models.CharField(blank=True, max_length=500, null=True)),
                ('fecha_fin_timbrado', models.CharField(blank=True, max_length=500, null=True)),
                ('ruc_empresa', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'verbose_name': 'Configuracion Empresa',
                'verbose_name_plural': 'Configuraciones Empresas',
                'permissions': (('add_confiempresa', 'Agregar Configuracion'), ('change_confiempresa', 'Editar Configuracion'), ('delete_confiempresa', 'Eliminar Configuracion'), ('view_confiempresa', 'Listar Configuraciones')),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_servicio', models.CharField(help_text='Ingrese nombre del servicio', max_length=200)),
                ('precio_servicio', models.CharField(help_text='Ingrese el precio del servicio', max_length=200)),
                ('min_serv', models.CharField(max_length=200)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('is_active', models.CharField(blank=True, default='S', max_length=200, null=True)),
            ],
            options={
                'verbose_name': 'Servicio',
                'verbose_name_plural': 'Servicios',
                'permissions': (('add_servicio', 'Agregar Servicio'), ('change_servicio', 'Editar Servicio'), ('delete_servicio', 'Eliminar Servicio'), ('view_servicio', 'Listar Servicios')),
                'default_permissions': (),
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
                'permissions': (('add_empleado', 'Agregar Empleado'), ('change_empleado', 'Editar Empleado'), ('delete_empleado', 'Eliminar Empleado'), ('view_empleado', 'Listar Empleados')),
                'default_permissions': (),
            },
        ),
    ]
