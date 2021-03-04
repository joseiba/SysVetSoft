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


    def __str__(self):
        """Formato del tipo producto"""
        return '{0}'.format(self.nombre_tipo)

    def get_absolute_url(self):
        """Retorna el URL para acceder a una instancia de un tipo de producto en particular."""
        return reverse('ciudad-detail', args=[str(self.id)])


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

    nombre_producto = models.CharField(max_length = 200, help_text = "Ingrese nombre del producto")
    descripcion = models.CharField(max_length = 200, help_text = "Ingrese descripcion del producto")
    fecha_vencimiento = models.DateField(help_text = "Ingrese fecha de vencimiento", null=True, blank=True, default='11/11/1111')
    fecha_baja = models.DateField(help_text = "Ingrese fecha de baja", null=True, blank=True, default='11/11/1111')
    fecha_movimiento = models.DateField(help_text = "Ingrese fecha de movimiento", null=True, blank=True, default='11/11/1111')
    tipo_producto = models.ForeignKey('TipoProducto', on_delete=models.SET_NULL)
    fecha_compra = models.DateField(help_text = "Ingrese fecha de compra")
    precio_compra = models.IntegerField(max_length = 7, help_text = 'Ingrese precio de compra')
    precio_venta = models.IntegerField(max_length = 7, help_text = 'Ingrese precio de venta')
    ubicacion = models.CharField(max_length = 200, help_text = "Ingrese ubicacion del producto")
    stock = models.IntegerField(max_length = 7, help_text = 'Ingrese stock')
    stock_minimo = models.IntegerField(max_length = 7, help_text = 'Ingrese stock minimo')

    def __str__(self):
        """Formato del cliente"""
        return '{0}'.format(self.nombre_producto)

    def get_absolute_url(self):
        """Retorna el URL para acceder a una instancia de un cliente en particular."""
        return reverse('producto-detail', args=[str(self.id)])


class ProductoStock (models.Model):
    """
    Clase que define 
    """
    producto_stock = models.IntegerField(max_length = 7, help_text = 'Ingrese stock')
    id_deposito = models.ForeignKey('Deposito', on_delete=models.SET_NULL)
    id_producto = models.ForeignKey('Producto', on_delete=models.SET_NULL)


    def __str__(self):
        """Formato de la ciudad"""
        return '{0}'.format(self.descripcion)

    def get_absolute_url(self):
        """Retorna el URL para acceder a una instancia de un deposito en particular."""
        return reverse('deposito-detail', args=[str(self.id)])