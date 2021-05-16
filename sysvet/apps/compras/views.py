from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import math

from apps.compras.models import Proveedor, Pedido, FacturaCompra, FacturaDet, Pago
from apps.compras.forms import ProveedorForm, PedidoForm, FacturaCompraForm, FacturaDetalleForm
from apps.ventas.producto.models import Producto


# Create your views here.
@login_required()
def add_proveedor(request):
    form = ProveedorForm    
    if request.method == 'POST':
        form = ProveedorForm(request.POST) 
        if form.is_valid():           
            form.save()
            messages.success(request, 'Se ha agregado correctamente!')
            return redirect('/compra/listProveedor')
    context = {'form' : form}
    return render(request, 'compras/proveedor/add_proveedor_modal.html', context)

@login_required()
def edit_proveedor(request, id):
    proveedor = Proveedor.objects.get(id=id)
    form = ProveedorForm(instance=proveedor)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if not form.has_changed():
            messages.info(request, "No has hecho ningun cambio!")
            return redirect('/compra/listProveedor')
        if form.is_valid():
            proveedor = form.save(commit=False)
            proveedor.save()
            messages.success(request, 'Se ha editado correctamente!')
            return redirect('/compra/listProveedor')
    context = {'form' : form, 'proveedor': proveedor}
    return render(request, 'compras/proveedor/edit_proveedor_modal.html', context)

@login_required()
def list_proveedor(request):
    return render(request, "compras/proveedor/list_proveedor.html")

@login_required()
def list_proveedor_ajax(request):
    query = request.GET.get('busqueda')
    if query != "":
        proveedor = Proveedor.objects.exclude(is_active="N").filter(Q(nombre_proveedor__icontains=query) | Q(ruc_proveedor__icontains=query))
    else:
        proveedor = Proveedor.objects.exclude(is_active="N").order_by('-last_modified')

    total = proveedor.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        page = math.ceil(start / length) + 1
        per_page = length

        proveedor = proveedor[start:start + length]

    data = [{'id': pro.id, 'nombre': pro.nombre_proveedor, 'direccion': pro.direccion, 
    'ruc': pro.ruc_proveedor, 'telefono' : pro.telefono, 'email': pro.email } for pro in proveedor]        

    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response)

#Metodo para eliminar servicio
@login_required()
def delete_proveedor(request, id):
    proveedor = Proveedor.objects.get(id=id)
    if request.method == 'POST':
        proveedor.is_active = "N"
        proveedor.save()
        return redirect('/compra/listProveedor')
    context = {'proveedor': proveedor}
    return render(request, "compras/proveedor/baja_proveedor_modal.html", context)


def add_pedido():
    producto = Producto.objects.all()
    for pro in producto:
        pe = pro.id

        try:
            pedi = Pedido.objects.get(id_producto=pe)
            if pro.stock_minimo >= pro.stock:
                pedi.id_producto = pro
                pedi.is_active = "S"
                pedi.save()
            else:
                pedi.is_active = "N"
                pedi.save()

        except:
            if pro.stock_minimo >= pro.stock:
                pedido = Pedido()
                pedido.id_producto = pro
                pedido.cantidad_pedido = '-'
                pedido.save()            

@login_required()
def list_pedido(request):
    add_pedido()
    return render(request, "compras/pedidos/list_pedidos.html")

@login_required()
def list_pedido_ajax(request):
    query = request.GET.get('busqueda')
    if query != "":
        pedido = Pedido.objects.exclude(is_active="N").filter(Q(id_producto__nombre_producto__icontains=query))
    else:
        pedido = Pedido.objects.exclude(is_active="N").order_by('-last_modified')

    total = pedido.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        page = math.ceil(start / length) + 1
        per_page = length

        pedido = pedido[start:start + length]

    data = [{'id': pe.id, 'nombre': pe.id_producto.nombre_producto, 'precio': pe.id_producto.precio_compra, 
    'cantidad': pe.cantidad_pedido, 'stock': pe.id_producto.stock, 'fecha_pedido': pe.fecha_alta} for pe in pedido]        

    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response)

@login_required()
def edit_pedido(request, id):
    pedido = Pedido.objects.get(id=id)
    form = PedidoForm(instance=pedido)
    if request.method == 'POST':
        form = PedidoForm(request.POST, instance=pedido)
        print(form)
        if not form.has_changed():
            messages.info(request, "No has hecho ningun cambio!")
            return redirect('/compra/listPedido')
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.save()
            messages.success(request, 'Se ha editado correctamente!')
            return redirect('/compra/listPedido')
    context = {'form' : form, 'pedido': pedido}
    return render(request, 'compras/pedidos/edit_pedido_modal.html', context)


#Facturas compras
@login_required()
def add_factura_compra(request):
    form = FacturaCompraForm()
    data = {}
    if request.method == 'POST' and request.is_ajax():
        try:
            factura_dict = json.loads(request.POST['id_factura'])
            #print(factura_dict)
            try:
                factura = FacturaCompra()
                factura.nro_factura = factura_dict['nro_factura']
                factura.nro_timbrado = factura_dict['nro_timbrado']
                factura.id_proveedor = factura_dict['id_proveedor']
                factura.fecha_emision = datetime.strptime(factura_dict['fecha_emision'],"%d/%m/%Y")
                factura.fecha_vecimiento = datetime.strptime(factura_dict['fecha_emision'],"%d/%m/%Y")
                factura.estado = 'PENDIENTE'
                factura.total_iva = int(factura_dict['total_iva'])
                factura.total = int(factura_dict['total_factura'])
                factura.save()
                for i in factura_dict['products']:
                    detalle = FacturaDet()
                    detalle.id_factura = factura.id
                    detalle.id_pedido = i['codigo_producto']
                    detalle.cantidad = int(i['cantidad'])
                    detalle.descripcion = i['description']
                    detalle.save()
            except Exception as e:
                print(e)
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data,safe=False)
    context = {'form': form, 'calc_iva': 5}
    return render(request, 'compras/factura/add_factura_compra.html', context)

def get_detalle_factura(id):
    data = []
    try:
        detalles = FacturaDet.objects.filter(id_factura=id)
        for i in detalles:
            item = i.id_pedido.obtener_dict()
            item['description'] = i.descripcion
            item['cantidad'] = i.cantidad
            data.append(item)
    except:
        pass
    return data

@login_required()
def list_factura_compra(request):
    return render(request, 'compras/factura/list_facturas.html')

def list_facturas_ajax(request):
    query = request.GET.get('busqueda')
    if query != "":
        factCompra = FacturaCompra.objects.exclude(is_active="N").filter(Q(nro_factura__icontains=query))
    else:
        factCompra = FacturaCompra.objects.exclude(is_active="N").order_by('-last_modified')

    total = factCompra.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        page = math.ceil(start / length) + 1
        per_page = length

        factCompra = factCompra[start:start + length]

    data = [{'nro_factura': fc.nro_factura, 'fecha_emision': fc.fecha_emision, 'fecha_vecimiento': fc.fecha_vecimiento, 
    'proveedor': fc.id_proveedor.nombre_proveedor, 'im_total': fc.total} for fc in factCompra]

    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response)

@login_required()
@csrf_exempt
def search_pediddos_factura(request):
    data = {}
    try:
        print(request.method)
        print(request.POST['action'])
        term = request.POST['term']
        print(term)
        if (request.method == 'POST') and (request.POST['action'] == 'search_products'):
            print('entra')
            data = []
            prods = Pedido.objects.filter(id_producto__nombre_producto__icontains=term)[0:10]
            print(prods, term)
            for p in prods:
                print('entra 2')
                item = p.obtener_dict()
                print('entra 2')
                item['id'] = p.id
                producto_desc = '%s' % (p.id_producto.nombre_producto)
                item['text'] = producto_desc
                data.append(item)
    except Exception as e:
        data['error'] = str(e)

    return JsonResponse(data, safe=False)

