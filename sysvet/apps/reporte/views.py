from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

import json
from django.http import JsonResponse

from apps.utiles.views import cargar_productos_vendidos
from apps.utiles.models import ProductoVendido
from apps.ventas.producto.models import Producto

# Create your views here.
@login_required()
@permission_required('reporte.view_reporte')
def reporte_producto(request):
    return render(request, 'reporte/reporte_producto.html')
