from django.db import models

from apps.ventas.producto.models import Producto

# Create your models here.
class Proveedor(models.Model):
    """[summary]

    Args:
        models ([Proveedor]): [Contiene la informacion de los proveedores]
    """    
    nombre_proveedor = models.CharField(max_length=500, help_text="Ingrese nombre del proveedor")
    direccion = models.CharField(max_length=500, help_text="Ingrese la direccion")
    ruc_proveedor = models.CharField(max_length=500, default="-", help_text="Ingrese el ruc del proveedor")
    telefono = models.CharField(max_length = 200, help_text="Ingrese el telefono del proveedor")
    email = models.EmailField(max_length = 200, help_text = "Ingrese email del proveedor", null=True, blank=True, default="-")
    last_modified = models.DateTimeField(auto_now=True, blank=True)
    is_active = models.CharField(max_length=2, default="S", blank=True, null=True)

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"

    def __str__(self):
        return self.nombre_proveedor


class Pedido(models.Model):
    """[summary]

    Args:
        models ([Pedido]): [Contiene la informacion de los pedidos]
    """
    cantidad_pedido = models.CharField(max_length=500, blank=True, null=True, default="-")
    last_modified = models.DateTimeField(auto_now=True, blank=True)
    is_active = models.CharField(max_length=2, default="S", blank=True, null=True)
    id_producto = models.ForeignKey(Producto, on_delete=models.PROTECT, null=False)

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"

    def __str__(self):
        return self.id_proveedor.nombre_proveedor

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
    ('RECIBIDO', 'Recibido'),
    ('NORECIBIDO', 'No Recibido')]        

class FacturaCompra(models.Model):
    nro_factura = models.CharField(max_length=200, unique=True)
    fecha_emision = models.DateField()
    fecha_vecimiento = models.DateField()
    tipo_factura = models.BooleanField()  # true: contado false: credito
    estado = models.CharField(max_length=12, choices=ESTADOS_FACTURA, default=ESTADOS_FACTURA[0])
    monto_iva1 = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)  # 5%
    monto_iva2 = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)  # 10% preguntar si esta bien
    total = models.FloatField(default=0)
    exenta = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    id_proveedor = models.ForeignKey('Proveedor', on_delete=models.PROTECT)
    id_pago = models.ForeignKey(Pago, on_delete=models.PROTECT)

    def __str__(self):
        return 'Factura Compra: %s - Proveedor: %s' % (self.nro_factura, self.id_proveedor.razon_social)

    class Meta:
        verbose_name = 'Factura Compra'
        verbose_name_plural = 'Facturas Compras'


TIPO_IVA = [
    ('IVA5', '5%'),
    ('IVA10', '10%'),
    ('EXENTA', 'Exenta')
]


class FacturaDet(models.Model):
    id_factura = models.ForeignKey('FacturaCompra', on_delete=models.CASCADE)
    id_pedido = models.ForeignKey('Pedido', on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    precio = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    descripcion = models.CharField(max_length=200, blank=True)
    tipo_iva = models.CharField(max_length=10, choices=TIPO_IVA, default=TIPO_IVA[1])

    class Meta:
        ordering = ['id']      