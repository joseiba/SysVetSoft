from django.db import models
from datetime import datetime

# Create your models here.
date = datetime.now()
class TipoProducto (models.Model):
    """
    Clase que define la estructura de un tipo de producto
    """
    nombre_tipo = models.CharField(max_length = 200, help_text = "Ingrese nombre del tipo de producto")
    fecha_alta = models.CharField(max_length = 200, default = date.strftime("%d/%m/%Y %H:%M:%S hs"), editable = False)
    fecha_baja = models.CharField(max_length = 200, default = '-', null = True, blank = True)
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
    fecha_vencimiento = models.DateField(help_text = "Ingrese fecha de vencimiento", null=True, blank=True)
    fecha_baja = models.DateField(help_text = "Ingrese fecha de baja", null=True, blank=True)
    fecha_movimiento = models.DateField(help_text = "Ingrese fecha de movimiento", null=True, blank=True)
    tipo_producto = models.ForeignKey('TipoProducto', on_delete=models.CASCADE, null=False)
    fecha_compra = models.DateField(help_text = "Ingrese fecha de compra")
    precio_compra = models.IntegerField(help_text = 'Ingrese precio de compra')
    precio_venta = models.IntegerField( help_text = 'Ingrese precio de venta')
    stock_minimo = models.IntegerField(help_text = 'Ingrese stock minimo')
    stock = models.IntegerField(help_text = 'Ingrese stock minimo')
    is_active = models.CharField(max_length=2, default="S", blank=True, null=True)
    id_deposito = models.ForeignKey('Deposito', on_delete=models.CASCADE, null=False)

    def __str__(self):
        """Formato del producto"""
        return '{0}'.format(self.nombre_producto)

    def get_absolute_url(self):
        """Retorna el URL para acceder a una instancia de un producto en particular."""
        return reverse('producto-detail', args=[str(self.id)])


class ProductoStock (models.Model):
    """
    Clase que define 
    """
    producto_stock = models.IntegerField(help_text = 'Ingrese stock')
    id_deposito = models.ForeignKey('Deposito', on_delete=models.CASCADE, null=False)
    id_producto = models.ForeignKey('Producto', on_delete=models.CASCADE, null=False)


    def _str_(self):
        """Formato del Stock"""
        return '{0}'.format(self.id_producto.nombre_producto)

    def get_absolute_url(self):
        """Retorna el URL para acceder a una instancia de un  en particular."""
        return reverse('deposito-detail', args=[str(self.id)])