import json
import math
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from io import BytesIO
from reportlab.pdfgen import canvas
from django.views.generic import View
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.units import cm
from reportlab.lib import colors

from apps.caja.models import Caja
from apps.configuracion.models import ConfiEmpresa

# Create your views here.
@login_required()
@permission_required('caja.view_caja')
def list_cajas(request):
    return render(request, 'caja/apertura_caja.html')

@login_required()
def list_caja_ajax(request):
    query = request.GET.get('busqueda')
    if query != "":
        caja = Caja.objects.filter(Q(fecha_hora_alta__icontains=query))
    else:
        caja = Caja.objects.all()

    total = caja.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        page = math.ceil(start / length) + 1
        per_page = length

        caja = caja[start:start + length]

    data = [{'id': ca.id, 'fecha_alta': ca.fecha_hora_alta, 'saldo_inicial': ca.saldo_inicial, 
    'total_ingreso': ca.total_ingreso, 'total_egreso' : ca.total_egreso, 'saldo_entregar': ca.saldo_a_entregar } for ca in caja]        

    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response)


@login_required()
@permission_required('caja.add_caja')
def add_caja(request):
    monto_initial = get_config()
    apertura = Caja()
    apertura.saldo_inicial = monto_initial
    apertura.save()
    messages.success(request, 'Apertura de caja correctamente!')
    return redirect('/caja/listCajas/')



def get_config():
    try:
        confi = ConfiEmpresa.objects.get(id=1)
        monto_split = confi.apertura_caja_inicial.split('.')
        monto_formateado = ""
        for monto in monto_split:
            monto_formateado += monto
        return monto_formateado
    except Exception as e:
        print(e)
        return "300000"

