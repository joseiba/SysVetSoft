from django.db import models
from sysvet.settings import STATIC_URL, MEDIA_URL
from datetime import date, datetime
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import StringIO, BytesIO

from apps.ventas.cliente.models import Cliente

import sys

url_pets_image = 'project_static/other/images/test.jfif'
# Create your models here.
date = datetime.now()

class Especie(models.Model):      
    nombre_especie = models.CharField(max_length=200, default="-", help_text="Seleccione la especie")
    last_modified = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        verbose_name = "Especie"
        verbose_name_plural = "Especies"

    def __str__(self):
        return self.nombre_especie

class Raza(models.Model):      
        nombre_raza = models.CharField(max_length=200,default="-", help_text="Seleccione la raza")
        last_modified = models.DateTimeField(auto_now=True, blank=True)
        id_especie = models.ForeignKey('Especie', on_delete=models.CASCADE, null=False)
    
        class Meta:
            verbose_name = "Raza"
            verbose_name_plural = "Razas"
    
        def __str__(self):
            return self.nombre_raza  

class Mascota(models.Model):
    """[summary]

    Args:
        models ([Mascota]): [Contiene la informacion de las mascotas]
    """    
    nombre_mascota = models.CharField(max_length=200, help_text="Ingrese nombre de la mascota")
    tatuaje = models.CharField(max_length=200, default="-", null=True, blank=True,  help_text="Ingrese el tatuaje")
    MACHO = 'MAC'
    HEMBRA = 'HEB'    
    tipo_sexo =((MACHO, 'Macho'),
                (HEMBRA, 'Hembra'))

    sexo = models.CharField(max_length=15, choices=tipo_sexo, default="-", help_text="Seleccione el sexo")
    edad = models.CharField(max_length = 200, default = '-', null = True, blank = True)
    imagen = models.ImageField(upload_to='mascotas/fotos', null=True, blank=True, help_text="Ingrese una foto")
    peso = models.CharField(max_length = 200, help_text="Ingrese el peso de la mascota")
    fecha_nacimiento =  models.DateField(null = True, blank = True)
    color_pelaje = models.CharField(max_length=200, default = '-', null = True, blank = True, help_text="Ingrese el color de la mascota")
    last_modified = models.DateTimeField(auto_now=True, blank=True)
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
    def __str__(self):
        return self.nombre_mascota

    def get_profile(self):
        if self.imagen:
            return '{}{}'.format(MEDIA_URL, self.imagen)
        return '{}{}'.format(STATIC_URL, url_pets_image)
    
    def save(self, *args, **kwargs):
        is_new = not self.id
        super().save(*args, **kwargs)
        if is_new:
            FichaMedica.objects.create(id_mascota=self)
    

#Modelos de ficha medica

class FichaMedica(models.Model):
    """[summary]

    Args:
        models ([FichaMedica]): [Contiene la informacion de la fichas medicas]                
    """    
    fecha_create = models.DateTimeField(auto_now=True, blank=True)
    id_mascota = models.ForeignKey('Mascota', on_delete=models.CASCADE, null=False)
    
    class Meta:
        verbose_name = "Ficha Medica"
        verbose_name_plural = "Fichas Medicas"

    def __str__(self):
        return self.id_mascota.nombre_mascota
    
    def save(self, *args, **kwargs):
        is_new = not self.id
        super().save(*args, **kwargs)
        if is_new:
            Vacuna.objects.create(id_ficha_medica=self)
            Consulta.objects.create(id_ficha_medica=self)
            Antiparasitario.objects.create(id_ficha_medica=self)



class Vacuna(models.Model):
    """[summary]

    Args:
        models ([Vacuna]): [Contiene la informacion de la Vacuna]                
    """ 
    vacuna = models.CharField(max_length = 200, default = '-', null = True, blank = True)
    tipo_vacuna = models.CharField(max_length = 200, default = '-', null = True, blank = True)
    proxima_vacunacion = models.CharField(max_length = 200, default = '-', null = True, blank = True)
    id_ficha_medica = models.ForeignKey('FichaMedica', on_delete=models.CASCADE, null=False)

    class Meta:
        verbose_name = "Ficha Medica"
        verbose_name_plural = "Fichas Medicas"

    def __str__(self):
        return self.id_ficha_medica.id_mascota.nombre_mascota


class Consulta(models.Model):
    """[summary]

    Args:
        models ([Consulta]): [Contiene la informacion de la Consulta]                        
    """ 
    diagnostico = models.CharField(max_length = 500, default = '-', null = True, blank = True)
    tratamiento = models.CharField(max_length = 500, default = '-', null = True, blank = True)
    proximo_tratamiento = models.CharField(max_length = 500, default = '-', null = True, blank = True)
    medicamento = models.CharField(max_length = 500, default = '-', null = True, blank = True)
    fecha_ultima_consulta = models.DateField(null = True, blank = True)
    fecha_proxima_consulta = models.DateField(null = True, blank = True)
    id_ficha_medica = models.ForeignKey('FichaMedica', on_delete=models.CASCADE, null=False)
    
    class Meta:
        verbose_name = "Consulta"
        verbose_name_plural = "Consultas"

    def __str__(self):
        return self.id_ficha_medica.id_mascota.nombre_mascota


class Antiparasitario(models.Model):
    """[summary]

    Args:
        models ([Antiparasitario]): [Contiene la informacion de los antiparasitarios]                        
    """ 
    antiparasitario = models.CharField(max_length = 500, default = '-', null = True, blank = True)
    proximo_antiparasitario= models.CharField(max_length = 500, default = '-', null = True, blank = True)
    id_ficha_medica = models.ForeignKey('FichaMedica', on_delete=models.CASCADE, null=False)
    
    class Meta:
        verbose_name = "Antiparasitario"
        verbose_name_plural = "Antiparasitarios"

    def __str__(self):
        return self.id_ficha_medica.id_mascota.nombre_mascota


class HistoricoFichaMedica(models.Model):
    """[summary]

    Args:
        models ([HistoricoFichaMedica]): [Contiene la informacion del historico de la ficha medica]                        
    """
    vacuna = models.CharField(max_length = 200, default = '-', null = True, blank = True)
    tipo_vacuna = models.CharField(max_length = 200, default = '-', null = True, blank = True)
    proxima_vacunacion = models.CharField(max_length = 200, default = '-', null = True, blank = True)
    diagnostico = models.CharField(max_length = 500, default = '-', null = True, blank = True)
    tratamiento = models.CharField(max_length = 500, default = '-', null = True, blank = True)
    proximo_tratamiento = models.CharField(max_length = 500, default = '-', null = True, blank = True)
    medicamento = models.CharField(max_length = 500, default = '-', null = True, blank = True)
    fecha_ultima_consulta = models.DateField(null = True, blank = True)
    fecha_proxima_consulta = models.DateField(null = True, blank = True)
    antiparasitario = models.CharField(max_length = 500, default = '-', null = True, blank = True)
    proximo_antiparasitario = models.CharField(max_length = 500, default = '-', null = True, blank = True)
    peso = models.CharField(max_length = 200,default = '-', null = True, blank = True)
    last_modified = models.DateTimeField(auto_now=True, blank=True)
    id_ficha_medica = models.IntegerField(null = True, blank = True)

    class Meta:
        verbose_name = "Historico Ficha Medicas"
        verbose_name_plural = "Historicos Fichas Medicas"

    """def __str__(self):
        return self.id_ficha_medica.id_mascota.nombre_mascota"""

