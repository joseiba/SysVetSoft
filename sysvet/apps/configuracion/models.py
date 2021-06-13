from django.db import models
from datetime import date, datetime, timedelta

#Tupla dinamica para las horas
HORAS_SER = []
# Create your models here.
class ConfiEmpresa(models.Model):
    """
    Clase que define la la configuracion de la empresa
    """
    apertura_caja_inicial = models.CharField(max_length=200, blank=True, null=True)
    ubicacion_deposito_inicial =  models.CharField(max_length=200, blank=True, null=True)
    nombre_empresa = models.CharField(max_length=500, blank=True, null=True)
    direccion = models.CharField(max_length=500, blank=True, null=True)
    cuidad = models.CharField(max_length=500, blank=True, null=True)
    telefono = models.CharField(max_length=500, blank=True, null=True)
    nro_timbrado =  models.CharField(max_length=500, blank=True, null=True)
    fecha_inicio_timbrado = models.CharField(max_length=500, blank=True, null=True)
    fecha_fin_timbrado = models.CharField(max_length=500, blank=True, null=True)
    ruc_empresa = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        verbose_name = "Configuracion Empresa"
        verbose_name_plural = "Configuraciones Empresas"
        default_permissions =  ()
        permissions = (
            ('add_confiempresa', 'Agregar Configuracion'),
            ('change_confiempresa', 'Editar Configuracion'),
            ('delete_confiempresa', 'Eliminar Configuracion'),
            ('view_confiempresa', 'Listar Configuraciones'))        

    def __str__(self):
        """Formato de configurcion"""
        return '{0}'.format(self.id)

    # Create your models here.
class Servicio(models.Model):
    """
    Clase que define la estructura de un Servicio
    """
    nombre_servicio = models.CharField(max_length = 200, help_text = "Ingrese nombre del servicio")
    precio_servicio = models.CharField(max_length = 200, help_text = "Ingrese el precio del servicio")
    min_serv = models.CharField(max_length = 200)
    last_modified = models.DateTimeField(auto_now=True, blank=True)
    is_active = models.CharField(max_length=200, blank=True, null=True, default="S")


    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
        default_permissions =  ()
        permissions = (
            ('add_servicio', 'Agregar Servicio'),
            ('change_servicio', 'Editar Servicio'),
            ('delete_servicio', 'Eliminar Servicio'),
            ('view_servicio', 'Listar Servicios'))         

    def __str__(self):
        """Formato del servicio"""
        return '{0}'.format(self.nombre_servicio)

    def get_absolute_url(self):
        """Retorna el URL para acceder a una instancia de una ciudad en particular."""
        return reverse('servicio-detail', args=[str(self.id)])

    def obtener_dict(self):
        dict = {}
        dict['codigo_producto'] = self.id
        dict['nombre'] = self.nombre_servicio
        dict['description'] = self.nombre_servicio
        dict['precio'] = self.precio_servicio
        dict['tipo'] = 'S'
        return dict

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
        default_permissions =  ()
        permissions = (
            ('add_empleado', 'Agregar Empleado'),
            ('change_empleado', 'Editar Empleado'),
            ('delete_empleado', 'Eliminar Empleado'),
            ('view_empleado', 'Listar Empleados')) 

    def __str__(self):
        """Formato del empleado"""
        return '{0}'.format(self.nombre_emp)


class TipoVacuna(models.Model):
    nombre_vacuna =  models.CharField(max_length = 500, blank=True, null=True)
    periodo_aplicacion = models.CharField(max_length = 500, blank=True, null=True)
    class Meta:
        verbose_name = "Vacunas"
        verbose_name_plural = "Vacunas"
        default_permissions =  ()
        permissions = (
            ('add_tipovacuna', 'Agregar Vacuna'),
            ('change_tipovacuna', 'Editar Vacuna'),
            ('delete_tipovacuna', 'Eliminar Vacuna'),
            ('view_tipovacuna', 'Listar Vacunas')) 