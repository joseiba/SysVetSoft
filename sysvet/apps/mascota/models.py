from django.db import models

from sysvet.settings import STATIC_URL, MEDIA_URL
from datetime import date

url_pets_image = 'project_static/other/images/img_default.png'
# Create your models here.
class Mascota(models.Model):
    """[summary]

    Args:
        models ([Mascota]): [Contiene la informacion de las mascotas]
    """    
    nombre_mascota = models.CharField(max_length=200, help_text="Ingrese nombre de la mascota")
    tatuaje = models.CharField(max_length=200, null=True, default="-", blank=True,  help_text="Ingrese el tatuaje")
    MACHO = 'MAC'
    HEMBRA = 'HEB'    
    tipo_sexo =((MACHO, 'Macho'),
                (HEMBRA, 'Hembra'))

    sexo = models.CharField(max_length=15, choices=tipo_sexo, default="-", help_text="Seleccione el sexo")
    edad = models.IntegerField(null=True, blank=True, default=0, help_text="Ingrese la edad")
    imagen = models.ImageField(upload_to='mascotas/fotos', null=True, blank=True, help_text="Ingrese una foto")
    peso = models.IntegerField(help_text="Ingrese el peso" )
    fecha_nacimmiento = models.DateField(help_text="Ingrese la fecha de nacimiento", null=True, blank=True, default=date.today)

    def get_profile(self):
        if self.imagen:
            return '{}{}'.format(MEDIA_URL, self.imagen)
        return '{}{}'.format(STATIC_URL, url_pets_image)
