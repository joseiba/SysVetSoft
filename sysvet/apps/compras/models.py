from django.db import models

from apps.ventas.producto.models import Producto
from datetime import datetime


# Create your models here.
date = datetime.now()
class Proveedor(models.Model):
    """[summary]

    Args:
        models ([Proveedor]): [Contiene la informacion de los proveedores]
    """    
    nombre_proveedor = models.CharField(max_length=500, help_text="Ingrese nombre del proveedor")
    direccion = models.CharField(max_length=500, help_text="Ingrese la direccion")
    ruc_proveedor = models.CharField(max_length=500, default="-", help_text="Ingrese el ruc del proveedor")
    telefono = models.CharField(max_length = 500, help_text="Ingrese el telefono del proveedor")
    email = models.EmailField(max_length = 500, help_text = "Ingrese email del proveedor", null=True, blank=True, default="-")
    last_modified = models.DateTimeField(auto_now=True, blank=True)
    is_active = models.CharField(max_length=2, default="S", blank=True, null=True)

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"

    def __str__(self):
        return  'Proveedor: %s - ruc: %s' % (self.nombre_proveedor, self.ruc_proveedor)

class Pedido(models.Model):
    """[summary]

    Args:
        models ([Pedido]): [Contiene la informacion de los pedidos]
    """
    cantidad_pedido = models.CharField(max_length=500, blank=True, null=True, default="-")
    fecha_alta = models.CharField(max_length = 200, default = date.strftime("%d/%m/%Y %H:%M:%S hs"), editable = False)
    pedido_cargado = models.CharField(max_length=2, default="N", blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True)
    is_active = models.CharField(max_length=2, default="S", blank=True, null=True)
    id_producto = models.ForeignKey(Producto, on_delete=models.PROTECT, null=False)

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"

    def obtener_dict(self):
        dict = {}
        dict['codigo_producto'] = self.id
        dict['nombre'] = self.id_producto.nombre_producto
        dict['description'] = self.id_producto.descripcion
        dict['precio'] = self.id_producto.precio_compra
        dict['cantidad_pedido'] = self.cantidad_pedido
        return dict

    def __str__(self):
        return self.id_producto.nombre_producto        

class PedidoCabecera(models.Model):

    fecha_alta = models.CharField(max_length = 200, default = date.strftime("%d/%m/%Y"), editable = False)
    pedido_cargado = models.CharField(max_length=2, default="N", blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True)
    is_active = models.CharField(max_length=2, default="S", blank=True, null=True)

    class Meta:
        verbose_name = "Pedido Cabecera"
        verbose_name_plural = "Pedido Cabeceras"

    def __str__(self):
        return self.fecha_alta

class PedidoDetalle(models.Model):
    """Model definition for Pedido Detalle."""
    id_pedido_cabecera = models.ForeignKey('PedidoCabecera', on_delete=models.CASCADE)
    id_pedido = models.ForeignKey('Pedido', on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    descripcion = models.CharField(max_length=800, blank=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True)
    class Meta:
        """Meta definition for Pedido Detalle"""

        verbose_name = 'Pedido Detalle'
        verbose_name_plural = 'Pedido Detalle'

    def __str__(self):
        """Unicode representation of Pedido Detalle."""
        pass

class Pago(models.Model):
    """[summary]

    Args:
        models ([Pedido]): [Contiene la informacion de los pedidos]
    """
    metodo_pago = models.CharField(max_length=100)
    descripcion = models.TextField()

    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Plural"


ESTADOS_FACTURA = [
    ('PENDIENTE', 'Pendiente'),
    ('CANCELADO', 'Cancelado'),
    ('FINALIZADO', 'Finalizado'),
]        

class FacturaCompra(models.Model):
    nro_factura = models.CharField(max_length=500, null=True)
    nro_timbrado = models.CharField(max_length=500, null=True)
    fecha_emision = models.CharField(max_length=500, null=True)
    fecha_vencimiento = models.CharField(max_length=500, null=True)
    tipo_factura = models.BooleanField(default=True)
    estado = models.CharField(max_length=500, choices=ESTADOS_FACTURA, default=ESTADOS_FACTURA[0])
    total_iva = models.IntegerField(default=0)
    total = models.FloatField(default=0)
    factura_cargada_producto = models.CharField(max_length=2, default="N", blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True)
    is_active = models.CharField(max_length=2, default="S", blank=True, null=True)
    id_proveedor = models.ForeignKey('Proveedor', on_delete=models.CASCADE, null=True)
    id_pedido_cabecera = models.ForeignKey('PedidoCabecera', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return 'Factura Compra: %s - Proveedor: %s' % (self.nro_factura, self.id_proveedor)

    class Meta:
        verbose_name = 'Factura Compra'
        verbose_name_plural = 'Facturas Compras'

class FacturaDet(models.Model):
    id_factura = models.ForeignKey('FacturaCompra', on_delete=models.CASCADE)
    id_pedido = models.ForeignKey('Pedido', on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    descripcion = models.CharField(max_length=800, blank=True)
    

    class Meta:
        ordering = ['id']      