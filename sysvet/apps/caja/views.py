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
from apps.compras.models import FacturaCompra
from apps.ventas.factura.models import FacturaCabeceraVenta

# Create your views here.
date = datetime.now()
today = date.strftime("%d/%m/%Y")
su_pos = 0
su_efectivo = 0

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

    data = [{'id': ca.id, 'fecha_alta': ca.fecha_hora_alta, 'fecha_cierre': ca.fecha_cierre, 'saldo_inicial': ca.saldo_inicial, 
    'total_ingreso': ca.total_ingreso, 'total_egreso' : ca.total_egreso, 'saldo_entregar': ca.saldo_a_entregar, 'estado': ca.apertura_cierre } for ca in caja]        

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
    caja_abierta = Caja.objects.exclude(apertura_cierre="C").filter(fecha_alta=today)
    if caja_abierta.count() > 0:
        messages.success(request, 'Ya tienes una caja abierta!')
        return redirect('/caja/listCajas/')
    else:
        caja_cerrada = Caja.objects.exclude(apertura_cierre="A").filter(fecha_alta=today)
        if caja_cerrada.count() > 0:
            messages.success(request, 'Ya has hecho una apertura y cierre en el dia!')
            return redirect('/caja/listCajas/')
        else:
            apertura = Caja()
            apertura.saldo_inicial = monto_initial
            apertura.save()
            messages.success(request, 'Apertura de caja correctamente!')
            return redirect('/caja/listCajas/')


def cerrar_caja(request, id):
    try:
        caja_cierre = Caja.objects.get(id=id)
        if caja_cierre.apertura_cierre != "C":
            sum_total_compras = sum_factura_compra()
            sum_total_venta = sum_factura_venta()
            saldo_entregrar = sum_total_venta - sum_total_compras - caja_cierre.saldo_inicial
            caja_cierre.total_ingreso = sum_total_venta
            caja_cierre.total_egreso = sum_total_compras
            if saldo_entregrar > 0:
                caja_cierre.saldo_a_entregar = saldo_entregrar
            else:
                caja_cierre.saldo_a_entregar = 0
            caja_cierre.total_pos = su_pos
            caja_cierre.total_efectivo = su_efectivo
            caja_cierre.apertura_cierre = "C"
            caja_cierre.fecha_cierre = date.strftime("%d/%m/%Y %H:%M:%S hs")
            caja_cierre.save()
            messages.success(request, 'Cierre de caja correctamente!')
            return redirect('/caja/listCajas/')
        else:
            messages.success(request, 'Esta caja ya esta cerrada!')
            return redirect('/caja/listCajas/')
    except Exception as e:
        print(e)
        messages.success(request, 'Ha ocurrido un error!')
        return redirect('/caja/listCajas/')



def sum_factura_compra():
    try:
        factura = FacturaCompra.objects.exclude(factura_caja="S").filter(fecha_alta=today)
        sum_total = 0
        for fac in factura:
            sum_total += fac.total
            fac.factura_caja = "S"
            fac.save()
        return sum_total
    except Exception as e:
        print(e)
        return 0

def sum_factura_venta():
    try:
        factura = FacturaCabeceraVenta.objects.exclude(factura_caja="S").filter(fecha_alta=today)
        sum_total = 0
        for fac in factura:
            sum_total += fac.total
            """if fac.contado_pos == "C":
                su_efectivo += fac.total
            else:
                su_pos += fac.total"""
            fac.factura_caja = "S"
            fac.save()
        return sum_total
    except Exception as e:
        print(e)
        return 0


def get_config():
    try:
        confi = ConfiEmpresa.objects.get(id=1)
        monto_split = confi.apertura_caja_inicial.split('.')
        monto_formateado = ""
        for monto in monto_split:
            monto_formateado += monto
        return float(monto_formateado)
    except Exception as e:
        print(e)
        return 300000

