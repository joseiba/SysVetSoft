# Generated by Django 3.1.5 on 2021-04-16 02:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Deposito',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(help_text='Ingrese descripcion del deposito', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_producto', models.CharField(help_text='Ingrese codigo del producto', max_length=50)),
                ('nombre_producto', models.CharField(help_text='Ingrese nombre del producto', max_length=200)),
                ('descripcion', models.CharField(help_text='Ingrese descripcion del producto', max_length=200)),
                ('fecha_vencimiento', models.DateField(blank=True, help_text='Ingrese fecha de vencimiento', null=True)),
                ('fecha_baja', models.DateField(blank=True, help_text='Ingrese fecha de baja', null=True)),
                ('fecha_movimiento', models.DateField(blank=True, help_text='Ingrese fecha de movimiento', null=True)),
                ('fecha_compra', models.DateField(help_text='Ingrese fecha de compra')),
                ('precio_compra', models.IntegerField(help_text='Ingrese precio de compra')),
                ('precio_venta', models.IntegerField(help_text='Ingrese precio de venta')),
                ('stock_minimo', models.IntegerField(help_text='Ingrese stock minimo')),
                ('stock', models.IntegerField(help_text='Ingrese stock minimo')),
                ('is_active', models.CharField(blank=True, default='S', max_length=2, null=True)),
                ('id_deposito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='producto.deposito')),
            ],
        ),
        migrations.CreateModel(
            name='TipoProducto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_tipo', models.CharField(help_text='Ingrese nombre del tipo de producto', max_length=200)),
                ('fecha_alta', models.CharField(default='15/04/2021 22:10:02 hs', editable=False, max_length=200)),
                ('fecha_baja', models.CharField(blank=True, default='-', max_length=200, null=True)),
                ('is_active', models.CharField(blank=True, default='S', max_length=2, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductoStock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('producto_stock', models.IntegerField(help_text='Ingrese stock')),
                ('id_deposito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='producto.deposito')),
                ('id_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='producto.producto')),
            ],
        ),
        migrations.AddField(
            model_name='producto',
            name='tipo_producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='producto.tipoproducto'),
        ),
    ]
