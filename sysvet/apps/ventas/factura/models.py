from django.db import models
from datetime import datetime

from apps.ventas.producto.models import Producto
from apps.configuracion.models import Servicio
from apps.ventas.cliente.models import Cliente

# Create your models here.
date = datetime.now()
class ProductoServicios(models.Model):
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=False)
    id_servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, null=False)

    def _str_(self):
        """Formato del ProductoServicios"""
        return '{0}'.format(self.id)
    

    class Meta:
        default_permissions =  ()
        permissions = (
            ('add_productoservicios', 'Agregar Producto Servicios'),
            ('change_productoservicios', 'Editar Producto Servicios'),
            ('delete_productoservicios', 'Eliminar Producto Servicios'),
            ('view_productoservicios', 'Listar Productos y Servicios'))  

class PagoVenta(models.Model):
    """[summary]

    Args:
        models ([PagoVenta]): [Contiene la informacion de los PagoVenta]
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

class FacturaCabeceraVenta(models.Model):
    nro_timbrado = models.CharField(max_length=500, null=True)
    nro_factura = models.CharField(max_length=500, null=True)
    fecha_inicio_timbrado = models.CharField(max_length=500, null=True)
    fecha_fin_timbrado = models.CharField(max_length=500, null=True)
    ruc_empresa = models.CharField(max_length=500, null=True)
    fecha_emision = models.CharField(max_length=500, default = date.strftime("%d/%m/%Y"), null=True)
    tipo_factura = models.BooleanField(default=True)
    estado = models.CharField(max_length=500, choices=ESTADOS_FACTURA, default=ESTADOS_FACTURA[0])
    total_iva = models.IntegerField(default=0)
    total = models.FloatField(default=0)
    factura_cargada = models.CharField(max_length=2, default="N", blank=True, null=True)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True)
    is_active = models.CharField(max_length=2, default="S", blank=True, null=True)

    def __str__(self):
        return 'Factura Venta: %s - Cliente: %s' % (self.nro_factura, self.id_cliente)

    class Meta:
        verbose_name = 'Factura Venta'
        verbose_name_plural = 'Facturas Ventas'
        default_permissions =  ()
        permissions = (
            ('add_facturacabeceraventa', 'Agregar Factura Venta'),
            ('change_facturacabeceraventa', 'Editar Factura Venta'),
            ('delete_facturacabeceraventa', 'Anular Factura Venta'),
            ('view_facturacabeceraventa', 'Listar Facturas Ventas'))          

class FacturaDetalleVenta(models.Model):
    id_factura_venta = models.ForeignKey('FacturaCabeceraVenta', on_delete=models.CASCADE)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True)
    tipo = models.CharField(max_length=100, blank=True, null=True)
    cantidad = models.IntegerField()
    descripcion = models.CharField(max_length=800, blank=True)
    

    class Meta:
        ordering = ['id']     
