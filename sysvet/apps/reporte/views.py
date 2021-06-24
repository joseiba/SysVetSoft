from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, date

import json
from django.http import JsonResponse

from apps.utiles.views import (cargar_productos_vendidos, cargar_productos_comprados, cargar_ganacias_por_mes,
cargar_producto_vendido_mes, cargar_productos_comprado_mes, cargar_servicios_vendidos)
from apps.utiles.models import (ProductoVendido, ProductoComprados,ProductoCompradoMes, ProductoVendidoMes,
GananciaPorMes, ServicioVendido)
from apps.configuracion.models import ConfiEmpresa
from apps.ventas.producto.models import Producto
from apps.ventas.mascota.models import Mascota, HistoricoFichaMedica
from apps.ventas.cliente.models import Cliente

today = datetime.now()
hoy = date.today()
# Create your views here.
@login_required()
@permission_required('reporte.view_reporte')
def reporte_producto(request):
    cargar_productos_vendidos()
    return render(request, 'reporte/producto/reporte_producto.html')

def reporte_prod_vendido(request):
    query = request.GET.get('busqueda')
    label_producto_ven = []
    data_producto_ven = []
    mensaje = ""
    try:    
        if query != "":
            produc_vendidos = ProductoVendido.objects.filter(Q(id_producto__nombre_producto__icontains=query))
        else:
            produc_vendidos = ProductoVendido.objects.all()

        for pv in produc_vendidos:
            label_producto_ven.append(pv.id_producto.nombre_producto)
            data_producto_ven.append(pv.cantidad_vendida_total)

        mensaje = "OK"
    except Exception as e:
        pass
    response = {'label_producto_ven': label_producto_ven, 'data_producto_ven': data_producto_ven,'mensaje': mensaje}
    return JsonResponse(response)

@login_required()
@permission_required('reporte.view_reporte')
def reporte_producto_comprados(request):
    cargar_productos_comprados()
    return render(request, 'reporte/producto/reporte_producto_comprado.html')

def reporte_prod_comprado(request):
    query = request.GET.get('busqueda')
    label_producto_con = []
    data_producto_con = []
    mensaje = ""
    try:    
        if query != "":
            produc_compra = ProductoComprados.objects.filter(Q(id_producto__nombre_producto__icontains=query))
        else:
            produc_compra = ProductoComprados.objects.all()

        for pc in produc_compra:
            label_producto_con.append(pc.id_producto.nombre_producto)
            data_producto_con.append(pc.cantidad_comprada_total)

        mensaje = "OK"
    except Exception as e:
        pass

    response = {'label_producto_con': label_producto_con, 'data_producto_con': data_producto_con,'mensaje': mensaje}
    return JsonResponse(response)


@login_required()
@permission_required('reporte.view_reporte')
def reporte_productos_vendido_mes(request):
    cargar_producto_vendido_mes()
    return render(request, 'reporte/producto/reporte_producto_vendido_mes.html')

def get_producto_vendido_mes(request):
    query = request.GET.get('busqueda')
    label = []
    data = []
    mensaje = ""
    try:    
        if query != "":
            prod = ProductoVendidoMes.objects.filter(Q(label_mes__icontains=query))
        else:
            prod = ProductoVendidoMes.objects.all()

        for p in prod:
            label.append(p.label_mes)
            data.append(p.cantidad_vendida_total)

        mensaje = "OK"
    except Exception as e:
        pass

    response = {'label': label, 'data': data,'mensaje': mensaje}
    return JsonResponse(response)

@login_required()
@permission_required('reporte.view_reporte')
def reporte_productos_comprado_mes(request):
    cargar_productos_comprado_mes()
    return render(request, 'reporte/producto/reporte_producto_comprado_mes.html')

def get_producto_comprado_mes(request):
    query = request.GET.get('busqueda')
    label = []
    data = []
    mensaje = ""
    try:    
        if query != "":
            prod = ProductoCompradoMes.objects.filter(Q(label_mes__icontains=query))
        else:
            prod = ProductoCompradoMes.objects.all()

        for p in prod:
            label.append(p.label_mes)
            data.append(p.cantidad_comprada_total)

        mensaje = "OK"
    except Exception as e:
        pass

    response = {'label': label, 'data': data,'mensaje': mensaje}
    return JsonResponse(response)



@login_required()
@permission_required('reporte.view_reporte')
def reporte_ganancias_mes(request):
    cargar_ganacias_por_mes()
    return render(request, 'reporte/ganancias/reporte_ganancias_mes.html')


def get_ganancias_mes(request):
    query = request.GET.get('busqueda')
    label = []
    data = []
    mensaje = ""
    try:    
        if query != "":
            ganancias = GananciaPorMes.objects.filter(Q(label_mes__icontains=query))
        else:
            ganancias = GananciaPorMes.objects.all()

        for ga in ganancias:
            label.append(ga.label_mes)
            data.append(ga.total_mes)
        mensaje = "OK"
    except Exception as e:
        pass

    response = {'label': label, 'data': data,'mensaje': mensaje}
    return JsonResponse(response)

@login_required()
@permission_required('reporte.view_reporte')
def reporte_stock_minimo(request):
    return render(request, 'reporte/producto/reporte_stock_minimo.html')


def get_producto_minimo(request):
    query = request.GET.get('busqueda')
    prod_minimo = []
    if query != "":
        productos = Producto.objects.exclude(is_active="N").filter(Q(id__icontains=query) |Q(nombre_producto__icontains=query)).order_by('-last_modified')        
        productos = productos.exclude(servicio_o_producto="S")
        productos = productos.exclude(producto_vencido="S")
    else:
        productos = Producto.objects.exclude(is_active="N").order_by('-last_modified')
        productos = productos.exclude(servicio_o_producto="S")
        productos = productos.exclude(producto_vencido="S")

    for p in productos:
        if p.stock_minimo >= p.stock_total:
            prod_minimo.append(p)

    total =  len(prod_minimo)

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        page = math.ceil(start / length) + 1
        per_page = length

        prod_minimo = prod_minimo[start:start + length]

    data =[{'id': p.id, 'nombre': p.nombre_producto, 'descripcion': p.descripcion, 'stock_minimo': p.stock_minimo ,'stock_total': p.stock_total} for p in prod_minimo]        
        
    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response)

@login_required()
@permission_required('reporte.view_reporte')
def reporte_stock_a_vencer(request):
    return render(request, 'reporte/producto/reporte_stock_vencimiento.html')


def get_producto_vencimiento(request):
    query = request.GET.get('busqueda')
    prod_vencimiento = []

    try:
        confi = ConfiEmpresa.objects.get(id=1)
        dias_compare = confi.dias_a_vencer
    except Exception as e:
        dias_compare = 30
    
    if query != "":
        productos = Producto.objects.exclude(is_active="N").filter(Q(id__icontains=query) |Q(nombre_producto__icontains=query)).order_by('-last_modified')        
        productos = productos.exclude(servicio_o_producto="S")
    else:
        productos = Producto.objects.exclude(is_active="N").order_by('-last_modified')
        productos = productos.exclude(servicio_o_producto="S")

    for p in productos:
        if p.fecha_vencimiento is not None:
            if rest_dates(p.fecha_vencimiento) <= dias_compare:
                prod_vencimiento.append(p)

    total =  len(prod_vencimiento)

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        page = math.ceil(start / length) + 1
        per_page = length

        prod_vencimiento = prod_vencimiento[start:start + length]

    data =[{'id': p.id, 'nombre': p.nombre_producto, 'descripcion': p.descripcion, 'stock_total': p.stock_total, 
            'fecha_vencimiento': p.fecha_vencimiento, 'dias_vencimiento': rest_dates(p.fecha_vencimiento)} for p in prod_vencimiento]        
        
    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response)


@login_required()
@permission_required('reporte.view_reporte')
def reporte_servicio_vendido(request):
    cargar_servicios_vendidos()
    return render(request, 'reporte/producto/servicio_vendido.html')

def get_servicio_vendido(request):
    query = request.GET.get('busqueda')
    label = []
    data = []
    mensaje = ""
    try:    
        if query != "":
            produc_vendidos = ServicioVendido.objects.filter(Q(id_producto__nombre_producto__icontains=query))
        else:
            produc_vendidos = ServicioVendido.objects.all()

        for pv in produc_vendidos:
            label.append(pv.id_producto.nombre_producto)
            data.append(pv.cantidad_vendida_total)

        mensaje = "OK"
    except Exception as e:
        pass
    response = {'label': label, 'data': data, 'mensaje': mensaje}
    return JsonResponse(response)


@login_required()
@permission_required('reporte.view_reporte')
def list_proximas_vacunas(request):
    return render(request, 'reporte/mascota/list_proximas_vacunas.html')


def get_proximas_vacunas(request):
    query = request.GET.get('busqueda')
    ficha = []

    try:
        confi = ConfiEmpresa.objects.get(id=1)
        dias_compare = confi.dias_alert_vacunas
    except Exception as e:
        dias_compare = 30
    
    if query != "":
        list_historico = HistoricoFichaMedica.objects.filter(Q(id_mascota__nombre_mascota__icontains=query) 
                                                            |Q(id_mascota__id_cliente__nombre_cliente__icontains=query)
                                                            |Q(id_mascota__id_cliente__apellido_cliente__icontains=query))
    else:
        list_historico = HistoricoFichaMedica.objects.all()
    for f in list_historico:
        if f.fecha_proxima_aplicacion is not None:
            if rest_dates(f.fecha_proxima_aplicacion) <= dias_compare:
                ficha.append(f)

    total =  len(ficha)

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        page = math.ceil(start / length) + 1
        per_page = length

        ficha = ficha[start:start + length]

    data =[{'id': f.id, 'cliente':try_exception_cliente(f.id_mascota.id_cliente), 'mascota': f.id_mascota.nombre_mascota,
            'telefono': f.id_mascota.id_cliente.telefono, 'vacuna': f.proxima_vacunacion, 
                'fecha': f.fecha_proxima_aplicacion} for f in ficha]         
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

def rest_dates(fecha_vencimiento):
    try:
        fechaDate = datetime(today.year, today.month, today.day)
        fecha_vencimiento_split = fecha_vencimiento.split('/')          
        fecha_vencimiento_compare = date(int(fecha_vencimiento_split[2]), int(fecha_vencimiento_split[1]), int(fecha_vencimiento_split[0]))
        return (fecha_vencimiento_compare - hoy).days if (fecha_vencimiento_compare - hoy).days >= 0 else 0
    except Exception as e:
        return 0