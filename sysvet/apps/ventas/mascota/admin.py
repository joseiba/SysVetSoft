from django.contrib import admin

from .models import Mascota, Especie, Raza

# Register your models here.
admin.site.register(Mascota)
admin.site.register(Especie)
admin.site.register(Raza)

