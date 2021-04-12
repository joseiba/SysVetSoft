from django.db import models

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