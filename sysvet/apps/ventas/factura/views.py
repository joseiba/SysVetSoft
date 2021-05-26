import json
import math
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
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

from apps.ventas.factura.models import FacturaCabeceraVenta, FacturaDetalleVenta
from apps.ventas.factura.forms import FacturaDetalleVentaForm, FacturaCabeceraVentaForm
from apps.configuracion.models import ConfiEmpresa
# Create your views here.
@login_required()
def list_factura_ventas(request):
    return render(request, 'ventas/factura/list_facturas_ventas.html')

def list_facturas__ventas_ajax(request):
    query = request.GET.get('busqueda')
    if query != "":
        factVenta = FacturaCabeceraVenta.objects.exclude(is_active="N").filter(Q(nro_factura__icontains=query) | Q(nro_timbrado__icontains=query) | Q(id_cliente__nombre_cliente__icontains=query)).order_by('-last_modified')
    else:
        factVenta = FacturaCabeceraVenta.objects.exclude(is_active="N").order_by('-last_modified')

    total = factVenta.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        page = math.ceil(start / length) + 1
        per_page = length

        factVenta = factVenta[start:start + length]
    
    data= [{'id': fv.id,'nro_factura': fv.nro_factura, 'nro_timbrado': fv.nro_timbrado, 'fecha_emision': fv.fecha_emision, 
            'cliente': fv.id_cliente, 'im_total': fv.total}for fv in factVenta]     

    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response)

@login_required()
def add_factura_venta(request):
    form = FacturaCabeceraVentaForm()
    data = {}
    mensaje = ""
    if request.method == 'POST' and request.is_ajax():
        try:
            confi = ConfiEmpresa.objects.get(id=1) 
            factura_dict = json.loads(request.POST['factura'])
            try:
                factura = FacturaCabeceraVenta()
                factura.nro_factura = factura_dict['nro_factura']
                factura.nro_timbrado = factura_dict['nro_timbrado']
                factura.ruc_empresa = confi.ruc_empresa
                factura.fecha_inicio_timbrado = confi.fecha_inicio_timbrado
                factura.fecha_fin_timbrado = confi.fecha_fin_timbrado
                factura.id_cliente = factura_dict['cliente']
                factura.total_iva = int(factura_dict['total_iva'])
                factura.total = int(factura_dict['total_factura'])
                factura.save()
                for i in factura_dict['products']:
                    detalle = FacturaDetalleVenta()
                    detalle.id_factura_venta = factura.id
                    detalle.id_producto_servicio = i['codigo_producto']
                    detalle.cantidad = int(i['cantidad'])
                    detalle.descripcion = i['description']
                    detalle.save()
                response = {'mensaje':mensaje }
                return JsonResponse(response)
            except Exception as e:
                mensaje = 'error'
                response = {'mensaje':mensaje }
                return JsonResponse(response)
        except Exception as e:
            mensaje = 'error'
            response = {'mensaje':mensaje }
        return JsonResponse(response)
    context = {'form': form,  'calc_iva': 5, 'accion': 'E'}

    return render(request, 'ventas/factura/add_factura_ventas.html', context)
