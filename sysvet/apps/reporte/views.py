from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

import json
from django.http import JsonResponse

from apps.utiles.views import cargar_productos_vendidos, cargar_productos_comprados
from apps.utiles.models import ProductoVendido, ProductoComprados
from apps.ventas.producto.models import Producto

# Create your views here.
@login_required()
@permission_required('reporte.view_reporte')
def reporte_producto(request):
    cargar_productos_vendidos()
    cargar_productos_comprados()

    label_producto_ven = []
    data_producto_ven = []
    label_producto_con = []
    data_producto_con = []

    produc_vendidos = ProductoVendido.objects.all()

    for pv in produc_vendidos:
        label_producto_ven.append(pv.id_producto.nombre_producto)
        data_producto_ven.append(pv.cantidad_vendida_total)

    produc_compra = ProductoComprados.objects.all()

    for pc in produc_compra:
        label_producto_con.append(pc.id_producto.nombre_producto)
        data_producto_con.append(pc.cantidad_comprada_total)

    context = {'label_producto_ven': label_producto_ven, 'data_producto_ven': data_producto_ven,
                'label_producto_con': label_producto_con, 'data_producto_con': data_producto_con}
    return render(request, 'reporte/producto/reporte_producto.html', context)


