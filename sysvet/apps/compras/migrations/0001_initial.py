# Generated by Django 3.1.5 on 2021-05-17 01:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('producto', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='FacturaCompra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nro_factura', models.CharField(max_length=500)),
                ('nro_timbrado', models.CharField(max_length=500)),
                ('fecha_emision', models.CharField(max_length=200)),
                ('fecha_vencimiento', models.CharField(max_length=200)),
                ('tipo_factura', models.BooleanField(default=True)),
                ('estado', models.CharField(choices=[('PENDIENTE', 'Pendiente'), ('CANCELADO', 'Cancelado'), ('FINALIZADO', 'Finalizado')], default=('PENDIENTE', 'Pendiente'), max_length=12)),
                ('total_iva', models.IntegerField(default=0)),
                ('total', models.FloatField(default=0)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('is_active', models.CharField(blank=True, default='S', max_length=2, null=True)),
            ],
            options={
                'verbose_name': 'Factura Compra',
                'verbose_name_plural': 'Facturas Compras',
            },
        ),
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metodo_pago', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
            ],
            options={
                'verbose_name': 'Pago',
                'verbose_name_plural': 'Plural',
            },
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_proveedor', models.CharField(help_text='Ingrese nombre del proveedor', max_length=500)),
                ('direccion', models.CharField(help_text='Ingrese la direccion', max_length=500)),
                ('ruc_proveedor', models.CharField(default='-', help_text='Ingrese el ruc del proveedor', max_length=500)),
                ('telefono', models.CharField(help_text='Ingrese el telefono del proveedor', max_length=200)),
                ('email', models.EmailField(blank=True, default='-', help_text='Ingrese email del proveedor', max_length=200, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('is_active', models.CharField(blank=True, default='S', max_length=2, null=True)),
            ],
            options={
                'verbose_name': 'Proveedor',
                'verbose_name_plural': 'Proveedores',
            },
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_pedido', models.CharField(blank=True, default='-', max_length=500, null=True)),
                ('fecha_alta', models.CharField(default='16/05/2021 21:08:40 hs', editable=False, max_length=200)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('is_active', models.CharField(blank=True, default='S', max_length=2, null=True)),
                ('id_producto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='producto.producto')),
            ],
            options={
                'verbose_name': 'Proveedor',
                'verbose_name_plural': 'Proveedores',
            },
        ),
        migrations.CreateModel(
            name='FacturaDet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('descripcion', models.CharField(blank=True, max_length=200)),
                ('id_factura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compras.facturacompra')),
                ('id_pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compras.pedido')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='facturacompra',
            name='id_proveedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compras.proveedor'),
        ),
    ]
