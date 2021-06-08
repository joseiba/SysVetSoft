from django.db import models

from datetime import datetime


# Create your models here.
date = datetime.now()
class Caja(models.Model):
    """
    Clase que define la estructura de caja
    """

    fecha_hora_alta = models.CharField(max_length=500, default = date.strftime("%d/%m/%Y"), null=True)
    saldo_inicial = models.CharField(max_length=800, null=True, blank=True)
    total_ingreso = models.CharField(max_length=1000, null=True, blank=True)
    total_egreso = models.CharField(max_length=1000, null=True, blank=True)
    total_dia = models.CharField(max_length=1000, null=True, blank=True)
    saldo_a_entregar = models.CharField(max_length=1000, null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True)
    apertura_cierre = models.CharField(max_length=2, default="A", blank=True, null=True)        

    class Meta:
        default_permissions =  ()
        permissions = (
            ('add_caja', 'Agregar Caja'),
            ('change_caja', 'Editar Caja'),
            ('delete_caja', 'Eliminar Caja'),
            ('view_caja', 'Listar Cajas'))     
