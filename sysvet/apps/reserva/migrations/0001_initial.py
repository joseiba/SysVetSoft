from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mascota', '__first__'),
        ('configuracion', '0001_initial'),
        ('cliente', '0001_initial'),
        ('mascota', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(blank=True, default='-', help_text='Ingrese la descripción del la reserva', max_length=200, null=True)),
                ('fecha_reserva', models.DateField()),
                ('hora_reserva', models.CharField(max_length=200)),
                ('disponible_emp', models.CharField(blank=True, default='S', max_length=2, null=True)),
                ('estado_re', models.CharField(blank=True, choices=[('FIN', 'Finalizado'), ('CAN', 'Cancelado'), ('PEN', 'Pendiente')], default='PEN', help_text='Seleccione el estado', max_length=15, null=True)),
                ('color_estado', models.CharField(blank=True, default='light blue', max_length=200, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('is_active', models.CharField(blank=True, default='S', max_length=2, null=True)),
                ('id_cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cliente.cliente')),
                ('id_empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configuracion.empleado')),
                ('id_mascota', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mascota.mascota')),
                ('id_servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configuracion.servicio')),
            ],
            options={
                'verbose_name': 'Reserva',
                'verbose_name_plural': 'Reservas',
            },
        ),
    ]
