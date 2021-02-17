from django.db import models
from sysvet.settings import STATIC_URL, MEDIA_URL
from datetime import date
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import StringIO, BytesIO

from apps.ventas.cliente.models import Cliente

import sys

url_pets_image = 'project_static/other/images/test.jfif'
# Create your models here.


class Especie(models.Model):    
    CANINO = 'CAN'
    FELINO = 'FEL'    
    tipo_especies =((CANINO, 'Canino/a'),
                (FELINO, 'Felino/a'))
    nombre_especie = models.CharField(max_length=200, choices=tipo_especies, default="-", help_text="Seleccione la especie")

    class Meta:
        verbose_name = "Especie"
        verbose_name_plural = "Especies"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Especie_detail", kwargs={"pk": self.pk})

class Raza(models.Model):
    
        nombre_raza = models.CharField(max_length=200)
        id_especie = models.ForeignKey('Especie', on_delete=models.CASCADE, null=False)
    
        class Meta:
            verbose_name = "Raza"
            verbose_name_plural = "Razas"
    
        def __str__(self):
            return self.name
    
        def get_absolute_url(self):
            return reverse("Raza_detail", kwargs={"pk": self.pk})    

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
    edad = models.PositiveIntegerField(null=True, blank=True, default=0, help_text="Ingrese la edad")
    imagen = models.ImageField(upload_to='mascotas/fotos', null=True, blank=True, help_text="Ingrese una foto")
    peso = models.IntegerField(help_text="Ingrese el peso" )
    fecha_nacimmiento = models.DateField(help_text="Ingrese la fecha de nacimiento", null=True, blank=True, default='11/11/1111')
    id_raza = models.ForeignKey('Raza', on_delete=models.CASCADE, null=False)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=False)


    class Meta:
        verbose_name = "Mascota"
        verbose_name_plural = "Mascotas"

    '''def save(self, *args, **kwargs):
        # Opening the uploaded image
        img = Image.open(self.imagen)
        if :
            print("entro")
            super().save(*args, **kwargs)

        if img.height > 200 or img.width > 200:

            output_size = (200, 200)
            img.thumbnail(output_size)
            img = img.convert('RGB')

            output = BytesIO()
            img.save(output, format='JPEG')
            output.seek(0)

            # change the imagefield value to be the newley modifed image value
            self.imagen = InMemoryUploadedFile(output, 'ImageField',
                                            f'{self.imagen.name.split(".")[0]}.jpg',
                                            'image/jpeg', sys.getsizeof(output),
                                            None)

        super().save(*args, **kwargs)'''

    def get_profile(self):
        if self.imagen:
            return '{}{}'.format(MEDIA_URL, self.imagen)
        return '{}{}'.format(STATIC_URL, url_pets_image)
    
