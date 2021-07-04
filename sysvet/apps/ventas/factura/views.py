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
from apps.utiles.views import reset_nro_timbrado
from apps.caja.models import Caja

date = datetime.now()
today = date.strftime("%d/%m/%Y")

# Create your views here.
@login_required()
@permission_required('factura.view_facturacabeceraventa')
def list_factura_ventas(request):
    caja_abierta = Caja.objects.exclude(apertura_cierre="C").filter(fecha_alta=today)
    if caja_abierta.count() > 0:
        abierto = "S"
    else:
        abierto = "N"
    context = {'caja_abierta' : abierto}
    return render(request, 'ventas/factura/list_facturas_ventas.html', context)

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

@login_required()
@permission_required('factura.view_facturacabeceraventa')
def list_facturas_ventas_anuladas(request):    
    return render(request, 'ventas/factura/list_facturas_anuladas.html')


def list_facturas_anuladas_ventas_ajax(request):
    query = request.GET.get('busqueda')
    if query != "":
        factVenta = FacturaCabeceraVenta.objects.exclude(is_active="S").filter(Q(nro_factura__icontains=query) | Q(nro_timbrado__icontains=query) | Q(id_cliente__nombre_cliente__icontains=query) 
            | Q(id_cliente__cedula__icontains=query) | Q(id_cliente__ruc__icontains=query)).order_by('-last_modified')
    else:
        factVenta = FacturaCabeceraVenta.objects.exclude(is_active="S").order_by('-last_modified')

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
    confi_initial = ConfiEmpresa.objects.get(id=1)
    caja_abierta = Caja.objects.exclude(apertura_cierre="C").filter(fecha_alta=today)
    if caja_abierta.count() > 0:
        abierto = "S"
    else:
        abierto = "N" 
    if request.method == 'POST' and request.is_ajax():
        try:
            confi = ConfiEmpresa.objects.get(id=1) 
            factura_dict = json.loads(request.POST['factura'])
            try:
                factura = FacturaCabeceraVenta()
                factura.nro_factura = factura_dict['nro_factura']
                factura.nro_timbrado = confi.nro_timbrado
                factura.ruc_empresa = confi.ruc_empresa
                factura.contado_pos = factura_dict['contado_pos']
                factura.fecha_inicio_timbrado = confi.fecha_inicio_timbrado
                factura.fecha_fin_timbrado = confi.fecha_fin_timbrado
                cliente_id = Cliente.objects.get(id=factura_dict['cliente'])
                factura.id_cliente = cliente_id
                factura.total_iva = int(factura_dict['total_iva'])
                factura.total = int(factura_dict['total_factura'])
                factura.total_formateado = factura_dict['total_formated']
                factura.save()
                for i in factura_dict['products']:
                    detalle = FacturaDetalleVenta()
                    detalle.id_factura_venta = factura
                    producto_id = Producto.objects.get(id=i['codigo_producto'])
                    detalle.id_producto = producto_id
                    detalle.tipo = i['tipo']
                    detalle.cantidad = int(i['cantidad'])
                    detalle.descripcion = i['description']
                    detalle.subtotal = "Gs. " + "{:,}".format(int(i['subtotal'])).replace(",",".")
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
    nro_factura_initial = reset_nro_timbrado(confi_initial.nro_timbrado)
    context = {'form': form,  'calc_iva': 5, 'accion': 'A', 'confi': confi, 'nro_factura': str(nro_factura_initial), 'caja_abierta' : abierto}
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
                factura.total_formateado = factura_dict['total_formated']             
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


@login_required()
@permission_required('factura.view_facturacabeceraventa')
def ver_factura_anulada_venta(request, id):
    factVenta = FacturaCabeceraVenta.objects.get(id=id)
    form = FacturaCabeceraVentaForm(instance=factVenta)
    confi = get_confi()
    mensaje = ""
    context = {'form': form, 'det': json.dumps(get_detalle_factura(id)), 'accion': 'ANU', 'confi': confi, 'factVenta': factVenta}
    return render(request, 'ventas/factura/ver_factura_anulada_venta.html', context)

@login_required()
@permission_required('factura.delete_facturacabeceraventa')
def anular_factura_venta(request, id):
    factVenta = FacturaCabeceraVenta.objects.get(id=id)
    if request.method == 'POST':
        factVenta.is_active = "N"
        factVenta.save()
        return redirect("/factura/listFacturasVentas/")
    context = {"id": id}
    return render(request, "ventas/factura/anular_factura_venta_modal.html", context)


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


def validate_producto_stock(request):
    data = []
    mensaje = ""
    if request.method == 'POST' and request.is_ajax():
        try:
            factura_dict = json.loads(request.POST['factura'])
            for i in factura_dict['products']:
                if i['tipo'] == "P":
                    producto_id = Producto.objects.get(id=i['codigo_producto'])
                    if producto_id.stock_total < int(i['cantidad']):
                        data.append(producto_id.nombre_producto)
            if len(data) > 0:
                mensaje = "F"
                response = {'mensaje':mensaje, 'data': json.dumps(data)}
                return JsonResponse(response)
            else:
                mensaje = "OK"
                response = {'mensaje':mensaje}
                return JsonResponse(response)
        except Exception as e:
            mensaje = 'error'
            response = {'mensaje':mensaje }
            return JsonResponse(response)


def reporte_factura_venta_pdf(request, id):
    fact = FacturaCabeceraVenta.objects.get(id=id)
    confi = ConfiEmpresa.objects.get(id=1)
    #Indicamos el tipo de contenido a devolver, en este caso un pdf
    response = HttpResponse(content_type='application/pdf')
    #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
    buffer = BytesIO()
    #Canvas nos permite hacer el reporte con coordenadas X y Y
    pdf = canvas.Canvas(buffer)
    #Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
    #self.cabecera(pdf)
    #Con show page hacemos un corte de página para pasar a la siguiente
    #Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
    pdf.setFont("Helvetica", 18)
    #Dibujamos una cadena en la ubicación X,Y especificada
    pdf.drawString(210, 790, u"Factura Venta")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(30, 760, u"Fecha Emisión: " + fact.fecha_emision)
    pdf.drawString(30, 740, u"" + str(fact.id_cliente))
    pdf.drawString(30, 720, u"Direccion: " + fact.id_cliente.id_ciudad.nombre_ciudad + "," + fact.id_cliente.direccion)
    pdf.drawString(390, 760, u"Nro Factura: " + fact.nro_factura)
    pdf.drawString(390, 740, u"Teléfono: " + fact.id_cliente.telefono)
    y = 700
    tabla_report(pdf, y, id, fact)

    pdf.showPage()
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

def tabla_report(pdf, y, id, fact):
    #Creamos una tupla de encabezados para neustra tabla
    encabezados = ('Codigo', 'Producto', 'Descripción', 'Cantidad', 'Precio \n Unitario', 'SubTotal')

    detalle_fact = FacturaDetalleVenta.objects.filter(id_factura_venta=id)

    count_detalle = 2
    #Creamos una lista de tuplas que van a contener a las personas
    detalles = [(deta.id_producto.id, deta.id_producto.nombre_producto, 
                deta.id_producto.descripcion, deta.cantidad, "Gs. " + deta.id_producto.precio_venta, deta.subtotal) for deta in detalle_fact]

    detalles_extras = [('', '', '', '', '', '') for i in range(count_detalle)]

    detalle_orden =  Table([encabezados] + detalles + detalles_extras, colWidths=[2.5 * cm, 3 * cm, 7* cm, 2 * cm, 3 * cm, 3 * cm])
        #Aplicamos estilos a las celdas de la tabla
    detalle_orden.setStyle(TableStyle(
        [
            #La primera fila(encabezados) va a estar centrada
            ('ALIGN',(0,0),(3,0),'CENTER'),
            #Los bordes de todas las celdas serán de color negro y con un grosor de 1
            ('GRID', (0, 0), (-1, -1), 1, colors.black), 
            #El tamaño de las letras de cada una de las celdas será de 10
            ('FONTSIZE', (0, 0), (-1, -1), 10),
        ]
    ))

    position = int(((detalle_fact.count() + count_detalle) * 50 ) / (2))
    pdf.setFont("Helvetica", 12)
    pdf.drawString(480, ((680 - position)) , u"Total: " + fact.total_formateado,)
    #Establecemos el tamaño de la hoja que ocupará la tabla 
    detalle_orden.wrapOn(pdf, 800, 600)
    #Definimos la coordenada donde se dibujará la tabla
    detalle_orden.drawOn(pdf, 10, 700 - position)