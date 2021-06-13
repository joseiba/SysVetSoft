# Generated by Django 3.1.5 on 2021-06-12 23:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0008_auto_20210609_2322'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='stock_fisico',
        ),
        migrations.AlterField(
            model_name='producto',
            name='fecha_compra',
            field=models.CharField(default='12/06/2021', editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='tipoproducto',
            name='fecha_alta',
            field=models.CharField(default='12/06/2021 19:02:46 hs', editable=False, max_length=200),
        ),
        migrations.CreateModel(
            name='Inventario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock_fisico', models.IntegerField(blank=True, default=0, null=True)),
                ('diferencia', models.IntegerField(blank=True, default=0, null=True)),
                ('id_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='producto.producto')),
            ],
        ),
    ]