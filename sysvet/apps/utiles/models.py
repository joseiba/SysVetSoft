from django.db import models

from apps.ventas.producto.models import Producto

# Create your models here.
class Timbrado(models.Model):
    """[summary]

    Args:
        models ([Proveedor]): [Contiene la informacion de los proveedores]
    """    
    nro_timbrado = models.CharField(max_length=500, null=True, blank=True)
    fecha_inicio_timbrado = models.CharField(max_length=500, null=True, blank=True)
    fecha_fin_timbrado = models.CharField(max_length=500, null=True, blank=True)
    vencido = models.CharField(max_length=2, default="N", blank=True, null=True)

    def __str__(self):
        return  'Timbrado: ' % (self.nro_timbrado)


class ProductoVendido(models.Model):
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True)
    cantidad_vendida_total = models.FloatField(null=True, blank=True, default=0)


class ProductoComprados(models.Model):
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True)
    cantidad_comprada_total = models.FloatField(null=True, blank=True, default=0)