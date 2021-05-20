from django.db import models
from datetime import date, datetime, timedelta

#Tupla dinamica para las horas
HORAS_SER = []
# Create your models here.
class ConfiEmpresa(models.Model):
    """
    Clase que define la la configuracion de la empresa
    """
    apertura_caja_inicial = models.CharField(max_length=200, blank=True, null=True, default="-")
    ubicacion_deposito_inicial =  models.CharField(max_length=200, blank=True, null=True, default="-")

    class Meta:
        verbose_name = "Configuracion Empresa"
        verbose_name_plural = "Configuraciones Empresas"

    def __str__(self):
        """Formato de configurcion"""
        return '{0}'.format(self.id_confi)

    # Create your models here.
class Servicio(models.Model):
    """
    Clase que define la estructura de un Servicio
    """
    cod_serv = models.CharField(max_length=200)
    nombre_servicio = models.CharField(max_length = 200, help_text = "Ingrese nombre del servicio")
    precio_servicio = models.CharField(max_length = 200, help_text = "Ingrese el precio del servicio")
    min_serv = models.CharField(max_length = 200)
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

class Empleado(models.Model):
    nombre_emp = models.CharField(max_length=200)
    apellido_emp = models.CharField(max_length=200)
    ci_empe = models.CharField(max_length=200)
    disponible = models.BooleanField(blank=True, null=True, default=True)    
    last_modified = models.DateTimeField(auto_now=True, blank=True)
    is_active = models.CharField(max_length=200, blank=True, null=True, default="S")
    id_servicio = models.ForeignKey('Servicio', on_delete=models.CASCADE, null=False)

    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"

    def __str__(self):
        """Formato del empleado"""
        return '{0}'.format(self.nombre_emp)