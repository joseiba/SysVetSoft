from django.contrib import admin
from .models import TipoProducto
from .models import Producto
from .models import ProductoStock
from .models import Deposito

# Register your models here.
admin.site.register(TipoProducto)
admin.site.register(Producto)
admin.site.register(ProductoStock)
admin.site.register(Deposito)

