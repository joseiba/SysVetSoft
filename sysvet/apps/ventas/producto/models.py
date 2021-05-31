from django.db import models
from datetime import datetime

# Create your models here.
date = datetime.now()
class TipoProducto (models.Model):
    """
    Clase que define la estructura de un tipo de producto
    """
    opciones = (
        ('S', 'Si'),
        ('N', 'No'),
    )

    nombre_tipo = models.CharField(max_length = 200, help_text = "Ingrese nombre del tipo de producto")
    fecha_alta = models.CharField(max_length = 200, default = date.strftime("%d/%m/%Y %H:%M:%S hs"), editable = False)
    fecha_baja = models.CharField(max_length = 200, default = '-', null = True, blank = True)
    vence = models.CharField(max_length=2, choices=opciones, default="S", blank=True, null=True, help_text='El producto vence?')
    last_modified = models.DateTimeField(auto_now=True, blank=True)
    is_active = models.CharField(max_length=2, default="S", blank=True, null=True)

    def __str__(self):
        """Formato del tipo producto"""
        return '{0}'.format(self.nombre_tipo)

    def get_absolute_url(self):
        """Retorna el URL para acceder a una instancia de un tipo de producto en particular."""
        return reverse('tipoProducto-detail', args=[str(self.id)])


class Deposito (models.Model):
    """
    Clase que define la estructura de un deposito
    """
    descripcion = models.CharField(max_length = 200, help_text = "Ingrese descripcion del deposito")
    last_modified = models.DateTimeField(auto_now=True, blank=True)
    is_active = models.CharField(max_length=2, default="S", blank=True, null=True)


    def __str__(self):
        """Formato de la ciudad"""
        return '{0}'.format(self.descripcion)

    def get_absolute_url(self):
        """Retorna el URL para acceder a una instancia de un deposito en particular."""
        return reverse('deposito-detail', args=[str(self.id)])


class Producto (models.Model):
    """
    Clase que define la estructura de un producto
    """

    codigo_producto = models.CharField(max_length = 50, help_text = "Ingrese codigo del producto")
    nombre_producto = models.CharField(max_length = 200, help_text = "Ingrese nombre del producto")
    descripcion = models.CharField(max_length = 200, help_text = "Ingrese descripcion del producto")
    fecha_vencimiento = models.CharField(max_length = 200,null = True, blank = True)
    fecha_baja = models.CharField(max_length = 200, default = '-', null = True, blank = True)
    fecha_movimiento = models.CharField(max_length = 200, default ="-", blank = True)
    tipo_producto = models.ForeignKey('TipoProducto', on_delete=models.CASCADE, null=True)
    fecha_compra = models.CharField(max_length = 200, default = date.strftime("%d/%m/%Y"), editable = False)
    precio_compra = models.CharField(max_length = 500,help_text = 'Ingrese precio de compra')
    precio_venta = models.CharField(max_length = 500, help_text = 'Ingrese precio de venta')
    stock_minimo = models.IntegerField(help_text = 'Ingrese stock minimo')
    lote = models.CharField(max_length = 200, null = True, blank = True)
    stock = models.IntegerField(help_text = 'Ingrese stock minimo')
    stock_total = models.IntegerField(null=True, blank=True)
    stock_movido = models.IntegerField(blank = True, null=True, default=0)
    servicio_o_producto = models.CharField(max_length=2, default="P", blank=True, null=True)
    id_servicio = models.IntegerField(blank = True, null=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True)
    is_active = models.CharField(max_length=2, default="S", blank=True, null=True)
    id_deposito = models.ForeignKey('Deposito', on_delete=models.CASCADE, null=True)

    def __str__(self):
        """Formato del producto"""
        return '{0}'.format(self.nombre_producto)

    def get_absolute_url(self):
        """Retorna el URL para acceder a una instancia de un producto en particular."""
        return reverse('producto-detail', args=[str(self.id)])

    def obtener_dict(self):
        dict = {}
        dict['codigo_producto'] = self.id
        dict['nombre'] = self.nombre_producto
        dict['description'] = self.descripcion
        dict['precio'] = self.precio_venta
        dict['tipo'] = self.servicio_o_producto
        return dict


class ProductoStock (models.Model):
    """
    Clase que define el detalle de los producto que se han movidos
    """
    producto_stock = models.IntegerField(help_text = 'Ingrese stock')
    id_deposito = models.ForeignKey('Deposito', on_delete=models.CASCADE, null=False)
    id_producto = models.ForeignKey('Producto', on_delete=models.CASCADE, null=False)
    last_modified = models.DateTimeField(auto_now=True, blank=True)
    is_active = models.CharField(max_length=2, default="S", blank=True, null=True)


    def _str_(self):
        """Formato del Stock"""
        return '{0}'.format(self.id_producto.nombre_producto)

    def get_absolute_url(self):
        """Retorna el URL para acceder a una instancia de un  en particular."""
        return reverse('deposito-detail', args=[str(self.id)])