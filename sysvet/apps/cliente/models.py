from django.db import models

# Create your models here.
class Ciudad (models.Model):
    """
    Clase que define la estructura de una ciudad
    """
    nombre_ciudad = models.CharField(max_length = 200, help_text = "Ingrese nombre de la ciudad")

    class Meta:
        verbose_name = "Ciudad"
        verbose_name_plural = "Ciudades"

    def __str__(self):
        """Formato de la ciudad"""
        return '{0}'.format(self.nombre_ciudad)

    def get_absolute_url(self):
        """Retorna el URL para acceder a una instancia de una ciudad en particular."""
        return reverse('ciudad-detail', args=[str(self.id)])




class Cliente (models.Model):
    """
    Clase que define la estructura de un cliente
    """

    nombre_cliente = models.CharField(max_length = 200, help_text = "Ingrese nombre del cliente")
    apellido_cliente = models.CharField(max_length = 200, help_text = "Ingrese apellido del cliente")
    direccion = models.CharField(max_length = 200, help_text = "Ingrese apellido del cliente")
    cedula = models.CharField(max_length = 200, help_text = "Ingrese cedula del cliente")
    ruc = models.CharField(max_length = 200, help_text = "Ingrese ruc del cliente")
    telefono = models.CharField(max_length = 200, help_text = "Ingrese telefono del cliente")
    email = models.CharField(max_length = 200, help_text = "Ingrese email del cliente")
    id_ciudad = models.ForeignKey(Ciudad, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """Formato del cliente"""
        return '{0}'.format(self.nombre_cliente)

    def get_absolute_url(self):
        """Retorna el URL para acceder a una instancia de un cliente en particular."""
        return reverse('cliente-detail', args=[str(self.id)])