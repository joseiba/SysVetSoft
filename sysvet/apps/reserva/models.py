from django.db import models

from apps.ventas.mascota.models import Mascota


# Create your models here.
class Servicio(models.Model):
    """
    Clase que define la estructura de una ciudad
    """
    nombre_servicio = models.CharField(max_length = 200, help_text = "Ingrese nombre del servicio")
    precio_servicio = models.CharField(max_length = 200, help_text = "Ingrese el precio del servicio")
    last_modified = models.DateTimeField(auto_now=True, blank=True)
    is_active = models.CharField(max_length=200, blank=True, null=True, default="S")


    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"

    def __str__(self):
        """Formato del servicio"""
        return '{0}'.format(self.nombre_servicio)

    def get_absolute_url(self):
        """Retorna el URL para acceder a una instancia de una ciudad en particular."""
        return reverse('servicio-detail', args=[str(self.id)])


class Reserva(models.Model):
    """
    Clase que define la estructura de la reserva
    """
    descripcion = models.CharField(max_length=200, help_text = "Ingrese la descripción del la reserva", blank=True, null=True)
    fecha = models.DateField()
    hora = models.TimeField()
    id_servicio = models.ForeignKey('Servicio', on_delete=models.CASCADE, null=False)
    id_mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, null=False) 

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"

    def __str__(self):
        """Formato de reserva"""
        return '{0}'.format(self.id_mascota.nombre_mascota)

    def get_absolute_url(self):
        """Retorna el URL para acceder a una instancia de una reserva en particular."""
        return reverse('reserva-detail', args=[str(self.id)])
