from django.db import models
from datetime import datetime


from apps.ventas.producto.models import Producto
from apps.ventas.factura.models import FacturaCabeceraVenta

date = datetime.now()
# Create your models here.
class Timbrado(models.Model): 
    nro_timbrado = models.CharField(max_length=500, null=True, blank=True)
    fecha_inicio_timbrado = models.CharField(max_length=500, null=True, blank=True)
    fecha_fin_timbrado = models.CharField(max_length=500, null=True, blank=True)
    vencido = models.CharField(max_length=2, default="N", blank=True, null=True)

    def __str__(self):
        return  'Timbrado: ' % (self.nro_timbrado)

class Cedula(models.Model):
    nro_cedula = models.CharField(max_length=500, null=True, blank=True)
    fecha_alta = models.CharField(max_length=500, default = date.strftime("%d/%m/%Y %H:%M:%S hs"), null=True, blank=True)

class Ruc(models.Model):
    nro_ruc = models.CharField(max_length=500, null=True, blank=True)
    fecha_alta = models.CharField(max_length=500, default = date.strftime("%d/%m/%Y %H:%M:%S hs"), null=True, blank=True)

class ProductoVendido(models.Model):
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True)
    cantidad_vendida_total = models.FloatField(null=True, blank=True, default=0)


class ProductoComprados(models.Model):
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True)
    cantidad_comprada_total = models.FloatField(null=True, blank=True, default=0)

class ProductoVendidoMes(models.Model):
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True)
    numero_mes =  models.IntegerField(null=True, blank=True)
    label_mes = models.CharField(max_length=500, null=True, blank=True)
    anho =  models.CharField(max_length=500, null=True, blank=True)
    cantidad_vendida_total = models.FloatField(null=True, blank=True, default=0)

class ProductoCompradoMes(models.Model):
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True)
    numero_mes =  models.IntegerField(null=True, blank=True)
    label_mes = models.CharField(max_length=500, null=True, blank=True)
    anho =  models.CharField(max_length=500, null=True, blank=True)
    cantidad_comprada_total = models.FloatField(null=True, blank=True, default=0)

class ServicioVendido(models.Model):
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True)
    cantidad_vendida_total = models.FloatField(null=True, blank=True, default=0)

class GananciaPorMes(models.Model):
    numero_mes =  models.IntegerField(null=True, blank=True)
    label_mes = models.CharField(max_length=500, null=True, blank=True)
    anho = models.CharField(max_length=500, null=True, blank=True)
    total_mes = models.FloatField(null=True, blank=True)
    total_mes_formateado = models.CharField(max_length=600, null=True, blank=True)
    id_factura_venta = models.ForeignKey(FacturaCabeceraVenta, on_delete=models.CASCADE, null=True)


