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

from apps.ventas.factura.models import FacturaCabeceraVenta, FacturaDetalleVenta, ProductoServicios
from apps.ventas.factura.forms import FacturaDetalleVentaForm, FacturaCabeceraVentaForm
from apps.configuracion.models import ConfiEmpresa, Servicio
from apps.ventas.producto.views import Producto
from apps.ventas.cliente.models import Cliente
# Create your views here.
@login_required()
@permission_required('factura.view_facturacabeceraventa')
def list_factura_ventas(request):
    return render(request, 'ventas/factura/list_facturas_ventas.html')

def list_facturas__ventas_ajax(request):
    query = request.GET.get('busqueda')
    if query != "":
        factVenta = FacturaCabeceraVenta.objects.exclude(is_active="N").filter(Q(nro_factura__icontains=query) | Q(nro_timbrado__icontains=query) | Q(id_cliente__nombre_cliente__icontains=query) 
            | Q(id_cliente__cedula__icontains=query) | Q(id_cliente__ruc__icontains=query)).order_by('-last_modified')
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
            'cliente': try_exception_cliente(fv.id_cliente), 'im_total': fv.total}for fv in factVenta]     

    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response)

def try_exception_cliente(id):
    try:
        cli = Cliente.objects.get(id=id.id)
        if cli.ruc is None:
            ruc_cedula = cli.cedula
        else:
            ruc_cedula = cli.ruc
        return 'Nombre: ' + cli.nombre_cliente + " " + cli.apellido_cliente  +'</br> ' + 'Ruc/Cédula: ' + ruc_cedula
    except Exception as e:
        return '-'

@login_required()
@permission_required('factura.add_facturacabeceraventa')
def add_factura_venta(request):
    form = FacturaCabeceraVentaForm()
    confi = get_confi()
    data = {}
    mensaje = ""
    if request.method == 'POST' and request.is_ajax():
        try:
            confi = ConfiEmpresa.objects.get(id=1) 
            factura_dict = json.loads(request.POST['factura'])
            try:
                factura = FacturaCabeceraVenta()
                factura.nro_factura = factura_dict['nro_factura']
                factura.nro_timbrado = confi.nro_timbrado
                factura.ruc_empresa = confi.ruc_empresa
                factura.fecha_inicio_timbrado = confi.fecha_inicio_timbrado
                factura.fecha_fin_timbrado = confi.fecha_fin_timbrado
                cliente_id = Cliente.objects.get(id=factura_dict['cliente'])
                factura.id_cliente = cliente_id
                factura.total_iva = int(factura_dict['total_iva'])
                factura.total = int(factura_dict['total_factura'])
                factura.save()
                for i in factura_dict['products']:
                    detalle = FacturaDetalleVenta()
                    detalle.id_factura_venta = factura
                    producto_id = Producto.objects.get(id=i['codigo_producto'])
                    detalle.id_producto = producto_id
                    detalle.tipo = i['tipo']
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
    context = {'form': form,  'calc_iva': 5, 'accion': 'A', 'confi': confi}

    return render(request, 'ventas/factura/add_factura_ventas.html', context)

@login_required()
@permission_required('factura.change_facturacabeceraventa')
def edit_factura_venta(request, id):
    factVenta = FacturaCabeceraVenta.objects.get(id=id)
    form = FacturaCabeceraVentaForm(instance=factVenta)
    confi = get_confi()
    data = {}
    mensaje = ""
    if request.method == 'POST' and request.is_ajax():
        try:        
            factura_dict = json.loads(request.POST['factura'])
            try:
                factura = FacturaCabeceraVenta.objects.get(id=id)
                factura.nro_factura = factura_dict['nro_factura']
                cliente_id = Cliente.objects.get(id=factura_dict['cliente'])
                factura.id_cliente = cliente_id
                factura.estado = 'PENDIENTE'
                factura.nro_timbrado = confi.nro_timbrado
                factura.ruc_empresa = confi.ruc_empresa
                factura.fecha_inicio_timbrado = confi.fecha_inicio_timbrado
                factura.fecha_fin_timbrado = confi.fecha_fin_timbrado
                factura.total_iva = int(factura_dict['total_iva'])
                factura.total = int(factura_dict['total_factura'])                
                factura.save()
                detailFact = FacturaDetalleVenta.objects.filter(id_factura_venta=id)
                detailFact.delete()
                for i in factura_dict['products']:
                    detalle = FacturaDetalleVenta()
                    detalle.id_factura_venta = factura
                    producto_id = Producto.objects.get(id=i['codigo_producto'])
                    detalle.id_producto = producto_id
                    detalle.tipo = i['tipo']
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
    context = {'form': form, 'det': json.dumps(get_detalle_factura(id)), 'accion': 'E', 'confi': confi}
    return render(request, 'ventas/factura/edit_factura_venta.html', context)

def get_detalle_factura(id):
    data = []
    try:
        detalles = FacturaDetalleVenta.objects.filter(id_factura_venta=id)
        for i in detalles:
            item = i.id_producto.obtener_dict()
            item['description'] = i.descripcion
            item['cantidad'] = i.cantidad
            data.append(item)

    except Exception as e:
        pass
    return data



@csrf_exempt
def get_producto_servicio_factura(request):
    data = {}
    try:
        term = request.POST['term']
        if (request.method == 'POST') and (request.POST['action'] == 'search_products'):
            data = []
            prods = Producto.objects.exclude(is_active='N').filter(nombre_producto__icontains=term)[0:10]
            for p in prods:
                item = p.obtener_dict()
                item['id'] = p.id
                producto_desc = '%s %s' % ('Producto: ' + p.nombre_producto, 
                                        'Descripción: ' + p.descripcion)
                item['text'] = producto_desc
                data.append(item)    
    except Exception as e:
        data['error'] = str(e)
    return JsonResponse(data, safe=False)


def get_confi():
    try:
        confi_empresa = ConfiEmpresa.objects.get(id=1)
        return confi_empresa
    except Exception as e:
        pass
        return ""