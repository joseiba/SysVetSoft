from django.db import models
from datetime import datetime

# Create your models here.

class TipoProducto (models.Model):
    """
    Clase que define la estructura de un tipo de producto
    """
    nombre_tipo = models.CharField(max_length = 200, help_text = "Ingrese nombre del tipo de producto")
    fecha_alta = models.DateTimeField(default = datetime.now, editable = False)
    fecha_baja = models.DateTimeField(null = True, blank = True)


    def __str__(self):
        """Formato de la ciudad"""
        return '{0}'.format(self.nombre_tipo)

    def get_absolute_url(self):
        """Retorna el URL para acceder a una instancia de una ciudad en particular."""
        return reverse('ciudad-detail', args=[str(self.id)])