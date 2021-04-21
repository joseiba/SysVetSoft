from django.db import models

from apps.ventas.mascota.models import Mascota
from apps.ventas.cliente.models import Cliente
from apps.configuracion.models import Servicio

class Reserva(models.Model):
    """
    Clase que define la estructura de la reserva
    """
    descripcion = models.CharField(max_length=200, help_text = "Ingrese la descripción del la reserva", blank=True, null=True, default="-")
    fecha_reserva = models.DateField()
    hora_reserva = models.CharField(max_length=200)
    disponible_emp = models.CharField(max_length=2, default="S", blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True)
    is_active = models.CharField(max_length=2, default="S", blank=True, null=True)
    id_servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, null=False)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=False) 

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"

    def __str__(self):
        """Formato de reserva"""
        return '{0}'.format(self.id_mascota.nombre_mascota)

    def get_absolute_url(self):
        """Retorna el URL para acceder a una instancia de una reserva en particular."""
        return reverse('reserva-detail', args=[str(self.id)])
