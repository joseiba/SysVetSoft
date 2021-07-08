from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

import json
from django.http import JsonResponse

from apps.ventas.producto.forms import TipoProductoForm, DepositoForm, ProductoForm
from apps.ventas.producto.models import TipoProducto, Deposito, Producto, ProductoStock, Inventario, HistoricoProductoPrecio
from apps.compras.models import FacturaCompra, FacturaDet
from apps.ventas.factura.models import FacturaCabeceraVenta, FacturaDetalleVenta
from apps.configuracion.models import ConfiEmpresa

date = datetime.now()

#Metodo para agregar tipo producto
@login_required()
@permission_required('configuracion.add_confiempresa')
def add_tipo_producto(request):
    form = TipoProductoForm
    if request.method == 'POST':
        form = TipoProductoForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Tipo de producto agregado correctamente!')
            return redirect('/tipoProducto/list')
    context = {'form' : form}
    return render(request, 'ventas/producto/add_tipo_producto.html', context)


# Metodo para editar tipo producto
@login_required()
@permission_required('configuracion.change_confiempresa')
def edit_tipo_producto(request, id):
    tipo_producto = TipoProducto.objects.get(id=id)
    form = TipoProductoForm(instance=tipo_producto)
    if request.method == 'POST':
        form = TipoProductoForm(request.POST, instance=tipo_producto)
        if not form.has_changed():
            messages.info(request, "No ha hecho ningun cambio")
            return redirect('/tipoProducto/list/')
        if form.is_valid():
            tipo_producto = form.save(commit=False)
            tipo_producto.save()
            messages.add_message(request, messages.SUCCESS, 'Tipo de producto editado correctamente!')
            return redirect('/tipoProducto/list/')

    context = {'form': form, 'tipo_producto':tipo_producto}
    return render(request, 'ventas/producto/edit_tipo_producto.html', context)

# Metodo para dar de baja tipo producto
@login_required()
@permission_required('configuracion.delete_confiempresa')
def baja_tipo_producto(request, id):
    tipo_producto = TipoProducto.objects.get(id=id)
    try:
        producto = Producto.objects.get(tipo_producto=id)
    except:
        producto = None
    if request.method == 'POST':
        if producto is None:
            if tipo_producto.fecha_baja == "-":
                tipo_producto.is_active = "N"
                tipo_producto.fecha_baja = date.strftime("%d/%m/%Y %H:%M:%S hs")
                tipo_producto.save()
                return redirect('/tipoProducto/list/')
            else:
                messages.success(request, 'El tipo de producto ya fue dado de baja!')
                return redirect('/tipoProducto/list/')
        else:
            messages.success(request, 'Este tipo de producto está asociado a productos en stock!')
            return redirect('/tipoProducto/list/')
    context = {'tipo_producto':tipo_producto}
    return render(request, 'ventas/producto/baja_tipo_producto.html', context)

# Metodo para dar de alta tipo producto
@login_required()
@permission_required('configuracion.change_confiempresa')
def alta_tipo_producto(request, id):
    tipo_producto = TipoProducto.objects.get(id=id)
    if request.method == 'POST':
        if tipo_producto.fecha_baja != "-":
            tipo_producto.is_active = "Y"
            tipo_producto.fecha_baja = '-'
            tipo_producto.save()
            return redirect('/tipoProducto/list/')
        else:
            messages.success(request, 'El tipo de producto ya fue dado de alta!')
            return redirect('/tipoProducto/list/')
    context = {'tipo_producto':tipo_producto}
    return render(request, 'ventas/producto/alta_tipo_producto.html', context)
    

#Metodo para listar todos los tipos de producto
@login_required()
@permission_required('configuracion.view_confiempresa')
def list_tipo_producto(request):
    return render(request, "ventas/producto/list_tipo_producto.html")


@login_required()
def get_list_tipo_producto(request):
    query = request.GET.get('busqueda')
    if query:
        tipos_productos = TipoProducto.objects.filter(Q(nombre_tipo__icontains=query))
    else:
        tipos_productos = TipoProducto.objects.all()

    total = tipos_productos.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        page = math.ceil(start / length) + 1
        per_page = length

        tipos_productos = tipos_productos[start:start + length]

    data = [{'id': tp.id, 'nombre_tipo': tp.nombre_tipo, 'fecha_alta': tp.fecha_alta, 'fecha_baja': tp.fecha_baja } for tp in tipos_productos]        

    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response) 

#Metodo para la busqueda de tipo de producto
@login_required()
def search_tipo_producto(request):
    query = request.GET.get('q')
    
    paginator = Paginator(tipos_productos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = { 'page_obj': page_obj}
    return render(request, "ventas/producto/list_tipo_producto.html", context)

#Metodo para la busqueda de tipo de producto
@login_required()
def vence_si_no(request):
    tipo_producto = request.GET.get('tipo')
    tipo_producto_vence = TipoProducto.objects.get(id=tipo_producto)

    if tipo_producto_vence.vence == 'S':
        response = {
            'mensaje' : 'S'
        }

        return JsonResponse(response)
    
    response = {
        'mensaje' : 'N'
    }

    return JsonResponse(response)

#Metodo para agregar deposito
@login_required()
@permission_required('configuracion.add_confiempresa')
def add_deposito(request):
    form = DepositoForm
    if request.method == 'POST':
        form = DepositoForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Deposito agregado correctamente!')
            return redirect('/deposito/list')   
    context = {'form' : form}
    return render(request, 'ventas/producto/add_deposito.html', context)

# Metodo para editar deposito
@login_required()
@permission_required('configuracion.change_confiempresa')
def edit_deposito(request, id):
    deposito = Deposito.objects.get(id=id)
    form = DepositoForm(instance=deposito)
    if request.method == 'POST':
        form = DepositoForm(request.POST, instance=deposito)
        if not form.has_changed():
            messages.info(request, "No ha hecho ningun cambio")
            return redirect('/deposito/list/')
        if form.is_valid():
            deposito = form.save(commit=False)
            deposito.save()
            messages.add_message(request, messages.SUCCESS, 'El depósito se ha editado correctamente!')
            return redirect('/deposito/list/')

    context = {'form': form, 'deposito': deposito}
    return render(request, 'ventas/producto/edit_deposito.html', context)

    #Metodo para listar todos los depositos
@login_required()
@permission_required('configuracion.view_confiempresa')
def list_deposito(request):
    return render(request, "ventas/producto/list_deposito.html")


@login_required()
def get_list_deposito(request):
    query = request.GET.get('busqueda')
    if query:
        depositos = Deposito.objects.filter(Q(descripcion__icontains=query)).order_by('-last_modified')
    else:
        depositos = Deposito.objects.all().order_by('-last_modified')

    total = depositos.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        page = math.ceil(start / length) + 1
        per_page = length

        depositos = depositos[start:start + length]

    data = [{'id': de.id, 'descripcion': de.descripcion } for de in depositos]        

    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response) 

#Metodo para la busqueda de deposito
@login_required()
def search_deposito(request):
    query = request.GET.get('q')
    if query:
        depositos = Deposito.objects.filter(Q(descripcion__icontains=query)).order_by('-last_modified')
    else:
        depositos = Deposito.objects.all().order_by('-last_modified')
    paginator = Paginator(depositos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = { 'page_obj': page_obj}
    return render(request, "ventas/producto/list_deposito.html", context)


    #Metodo para agregar producto
@login_required()
@permission_required('producto.add_producto')
def add_producto(request):
    form = ProductoForm
    try:
        confiEm = ConfiEmpresa.objects.get(id=1)
        depo = Deposito.objects.get(descripcion=confiEm.ubicacion_deposito_inicial)
        if request.method == 'POST':
            form = ProductoForm(request.POST or None)
            if form.is_valid():                            
                pro = form.save(commit=False)                
                pro.stock_total = request.POST.get('stock')
                pro.save()
                messages.add_message(request, messages.SUCCESS, 'Producto agregado correctamente!')
                return redirect('/producto/add')  
    except:
        messages.add_message(request, messages.SUCCESS, 'Se debe agregar primeramente un deposito en configuraciones iniciales!')
        context = {'form' : form}
        return render(request, 'ventas/producto/add_producto.html', context)
    context = {'form' : form, 'deposito_inicial': depo.id}
    return render(request, 'ventas/producto/add_producto.html', context)

# Metodo para editar Productos
@login_required()
@permission_required('producto.change_producto')
def edit_producto(request, id):
    producto = Producto.objects.get(id=id)
    form = ProductoForm(instance=producto)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if not form.has_changed():
            messages.info(request, "No ha hecho ningun cambio")
            return redirect('/producto/edit/' + str(id))
        if form.is_valid():
            producto = form.save(commit=False)
            producto.stock_total = request.POST.get('stock')
            producto.save()
            messages.add_message(request, messages.SUCCESS, 'El producto se ha editado correctamente!')
            return redirect('/producto/edit/' + str(id))

    context = {'form': form, 'producto': producto}
    return render(request, 'ventas/producto/edit_producto.html', context)

# Metodo para editar Productos
@login_required()
@permission_required('producto.add_producto')
def mover_producto(request, id):
    producto_movido = Producto()
    producto_moved = ProductoStock()
    producto = Producto.objects.get(id=id)
    form = ProductoForm(instance=producto)
    if request.method == 'POST':
        nombre_deposito = request.POST.get('id_deposito')
        cantidad = request.POST.get('stock')
        deposito = Deposito.objects.get(id=nombre_deposito)

        if producto.stock - int(cantidad) >= 0:
            producto.stock = producto.stock - int(cantidad)
        else:
            producto.stock = 0
        producto.save() 

        if int(cantidad) >= 0:
            producto_moved.producto_stock = int(cantidad)
        else:
            producto_moved.producto_stock = 0
        producto_moved.id_deposito = deposito
        producto_moved.id_producto = producto
        producto_moved.save()
        messages.add_message(request, messages.SUCCESS, 'El producto se ha movido correctamente!')

        return redirect('/producto/listDetalle/' + str(id))

    context = {'form': form, 'producto': producto}
    return render(request, 'ventas/producto/mover_producto.html', context)

#Metodo para eliminar producto
@login_required()
@permission_required('producto.delete_producto')
def delete_producto(request, id):
    producto = Producto.objects.get(id=id)
    producto.is_active = "N"
    producto.save()
    return redirect('/producto/listGeneral/')

#Metodo para listar todos los productos
def add_factura_to_producto():
    facturaCompra = FacturaCompra.objects.all()
    if facturaCompra is not None:
        for factCom in facturaCompra:
            if(factCom.facturado == 'S'):
                if(factCom.factura_cargada_producto == 'N'):
                    factCom.factura_cargada_producto = 'S'
                    factCom.save()
                    facDe = FacturaDet.objects.filter(id_factura=factCom.id)
                    for factDet in facDe:
                        try:                        
                            prod = Producto.objects.get(id=factDet.id_producto.id)
                            prod.fecha_compra = date.strftime("%d/%m/%Y")
                            prod.precio_compra = factDet.id_producto.precio_compra
                            prod.stock = prod.stock + factDet.cantidad
                            prod.stock_total = prod.stock_total + factDet.cantidad
                            prod.save()
                        except Exception as e:
                            pass

def rest_factura_venta_to_producto():
    factVenta = FacturaCabeceraVenta.objects.all()
    if factVenta is not None:
        for fv in factVenta:
            if(fv.factura_cargada == 'N'):
                fv.factura_cargada = 'S'
                fv.save()
                facDe = FacturaDetalleVenta.objects.filter(id_factura_venta=fv.id)
                for factDet in facDe:
                    try:
                        if factDet.tipo == 'P':
                            prod = Producto.objects.get(id=factDet.id_producto.id)
                            prod.fecha_compra = date.strftime("%d/%m/%Y")
                            if prod.stock - factDet.cantidad >= 0:
                                prod.stock = prod.stock - factDet.cantidad
                            else:
                                prod.stock = 0

                            if prod.stock_total - factDet.cantidad >= 0:
                                prod.stock_total = prod.stock_total - factDet.cantidad
                            else:
                                prod.stock_total = 0
                            
                            prod.save()
                    except Exception as e:
                        pass



def sum_anular_factura_venta_to_producto():
    factVenta = FacturaCabeceraVenta.objects.exclude(is_active="S").all()
    if factVenta is not None:
        for fv in factVenta:
            if(fv.factura_anulada == 'N'):
                fv.factura_anulada = "S"
                fv.save()
                facDe = FacturaDetalleVenta.objects.filter(id_factura_venta=fv.id)
                for factDet in facDe:
                    try:
                        if factDet.tipo == 'P':
                            prod = Producto.objects.get(id=factDet.id_producto.id)
                            prod.stock = prod.stock + factDet.cantidad
                            prod.stock_total = prod.stock_total + factDet.cantidad                            
                            prod.save()
                    except Exception as e:
                        pass


@login_required()
@permission_required('producto.view_producto')
def list_producto(request,id):
    data = []
    data_detalle = []
    stock_movido_cero = 0
    try:
        product = Producto.objects.filter(id=id)

        data =[{'id': p.id, 'nombre': p.nombre_producto, 'descripcion': p.descripcion, 'stock_actual': p.stock, 
            'deposito': p.id_deposito.descripcion} for p in product]

        pro = Producto.objects.get(id=id)
        stock_movido_cero = pro.stock      
    except Exception as e:
        pass

    try:
        producto_detalle = ProductoStock.objects.filter(id_producto=id)
        data_detalle =[{'id': p.id, 'codigo': p.id_producto.id ,'nombre': p.id_producto.nombre_producto, 'descripcion': p.id_producto.descripcion, 
        'stock_movido': p.producto_stock, 'deposito': p.id_deposito.descripcion} for p in producto_detalle]
    except Exception as e:
        pass   

    context = {'producto_detalle': data, 'producto_movido': data_detalle, 'id_producto': id, 'stck_cero': stock_movido_cero}
    return render(request, "ventas/producto/list_producto.html", context)

#Metodo para la busqueda de productos
@login_required()
def search_producto(request):
    query = request.GET.get('q')
    if query:
        productos = Producto.objects.filter(Q(nombre_producto__icontains=query) | Q(codigo_producto__icontains=query) | Q(id_deposito__descripcion__icontains=query)).order_by('-last_modified')
    else:
        productos = Producto.objects.all().order_by('-last_modified')
    paginator = Paginator(productos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = { 'page_obj': page_obj}
    return render(request, "ventas/producto/list_producto.html", context)

@permission_required('producto.add_producto')
def mover_producto_detalle_general(request, id):
    try:
        pedido_trasladado = ProductoStock.objects.get(id=id)
        producto_general = Producto.objects.get(id=pedido_trasladado.id_producto.id)
        producto_general.stock = producto_general.stock + pedido_trasladado.producto_stock
        producto_general.stock_total = producto_general.stock
        producto_general.save()
        pedido_trasladado.delete()
        messages.add_message(request, messages.SUCCESS, 'El producto se ha movido correctamente a la lista general!')
        return redirect('/producto/listDetalle/' + str(pedido_trasladado.id_producto.id))
    except Exception as e:
        messages.add_message(request, messages.SUCCESS, 'ha ocurrido un error inesperado, intente más tarde!')        
        return redirect('/producto/listGeneral/')

@login_required()
@permission_required('producto.view_producto')
def list_productos_general(request):
    add_factura_to_producto()
    rest_factura_venta_to_producto()
    sum_anular_factura_venta_to_producto()
    poner_vencido_producto()
    return render(request, "ventas/producto/list_producto_general.html")


@login_required()
def list_producto_general_ajax(request):
    query = request.GET.get('busqueda')
    if query != "":
        productos = Producto.objects.exclude(is_active="N").filter(Q(id__icontains=query) |Q(nombre_producto__icontains=query)).order_by('-last_modified')        
        productos = productos.exclude(servicio_o_producto="S")
        productos = productos.exclude(producto_vencido="S")
    else:
        productos = Producto.objects.exclude(is_active="N").order_by('-last_modified')
        productos = productos.exclude(servicio_o_producto="S")
        productos = productos.exclude(producto_vencido="S")


    total = productos.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        page = math.ceil(start / length) + 1
        per_page = length

        productos = productos[start:start + length]

    data =[{'id': p.id, 'nombre': p.nombre_producto, 'descripcion': p.descripcion, 'stock_total': p.stock_total} for p in productos]        
        
    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response)

def list_producto_vencido_ajax(request):
    query = request.GET.get('busqueda')
    if query != "":
        productos = Producto.objects.exclude(is_active="N").filter(Q(nombre_producto__icontains=query) | Q(id__icontains=query)).order_by('-last_modified')        
        productos = productos.exclude(servicio_o_producto="S")
        productos = productos.exclude(producto_vencido="N")
    else:
        productos = Producto.objects.exclude(is_active="N").order_by('-last_modified')
        productos = productos.exclude(servicio_o_producto="S")
        productos = productos.exclude(producto_vencido="N")


    total = productos.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        page = math.ceil(start / length) + 1
        per_page = length

        productos = productos[start:start + length]

    data =[{'id': p.id, 'nombre': p.nombre_producto, 'descripcion': p.descripcion, 'stock_vencido': p.stock_total, 
    'fecha_vencimiento': p.fecha_vencimiento} for p in productos]        
        
    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response)

def poner_vencido_producto():
    produc = Producto.objects.exclude(is_active="N").all()
    produc = produc.exclude(producto_vencido="S").all()
    today = datetime.now()
    fechaDate = datetime(today.year, today.month, today.day)
    if produc is not None:
        try:
            for p in produc:
                if p.fecha_vencimiento is not None:
                    fecha_vencimiento_split = p.fecha_vencimiento.split('/')
                    fecha_vencimiento_compare = datetime(int(fecha_vencimiento_split[2]), int(fecha_vencimiento_split[1]), int(fecha_vencimiento_split[0]))
                    if fechaDate > fecha_vencimiento_compare:
                        p.producto_vencido = "S"
                        p.is_active = "N"
                        p.save()
        except Exception as e:
            pass



# Ajuste de Inventario
@login_required()
@permission_required('producto.view_inventario')
def list_ajustar_inventario(request):
    add_factura_to_producto()
    rest_factura_venta_to_producto()
    sum_anular_factura_venta_to_producto()
    poner_vencido_producto()
    return render(request, "ventas/producto/inventario/list_ajuste_inventario.html")


def list_ajuste_inventario_ajax(request):
    query = request.GET.get('busqueda')
    if query != "":
        productos = Producto.objects.exclude(is_active="N").filter(Q(id__icontains=query) |Q(nombre_producto__icontains=query) |Q(tipo_producto__nombre_tipo__icontains=query)).order_by('-last_modified')        
        productos = productos.exclude(servicio_o_producto="S")
        productos = productos.exclude(producto_vencido="S")
        productos = productos.exclude(stock_total=0)
    else:
        productos = Producto.objects.exclude(is_active= "N").order_by('-last_modified')
        productos = productos.exclude(servicio_o_producto="S")
        productos = productos.exclude(producto_vencido="S")
        productos = productos.exclude(stock_total=0)


    total = productos.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        page = math.ceil(start / length) + 1
        per_page = length

        productos = productos[start:start + length]

    data =[{'id': p.id, 'nombre': p.nombre_producto, 'descripcion': p.descripcion, 'stock_total': p.stock_total,
            'stock_fisico': 0} for p in productos]        
        
    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response)

@login_required()
@permission_required('producto.add_inventario')
def add_ajuste_inventario(request):
    mensaje = ""
    if request.method == 'POST' and request.is_ajax():
        try:
            ajustes_dict = json.loads(request.POST['ajuste'])
            try:
                for i in ajustes_dict['products']:
                    inve = Inventario()
                    producto_id = Producto.objects.get(id=i['codigo_producto'])
                    inve.id_producto = producto_id
                    inve.stock_fisico = int(i['cantidad'])
                    inve.stock_viejo = producto_id.stock_total
                    inve.diferencia = int(i['cantidad']) - producto_id.stock_total 
                    producto_id.stock_total = int(i['cantidad'])
                    producto_id.stock = int(i['cantidad'])
                    inve.save()
                    producto_id.save()
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
    return render(request, 'ventas/producto/inventario/add_ajuste_inventario.html')


@login_required()
@csrf_exempt
def get_producto_inventario(request):
    data = {}
    try:
        term = request.POST['term']
        if (request.method == 'POST') and (request.POST['action'] == 'search_products'):
            data = []
            prods = Producto.objects.exclude(is_active='N').all()
            prods = prods.exclude(stock_total=0).all()
            prods = prods.exclude(servicio_o_producto="S").filter(nombre_producto__icontains=term)[0:10]
            for p in prods:
                item = p.obtener_dict()
                item['id'] = p.id
                producto_desc = '%s %s' % ('Producto: ' + p.nombre_producto ,
                                        'Descripción: ' + p.descripcion)
                item['text'] = producto_desc
                data.append(item)
    except Exception as e:
        data['error'] = str(e)

    return JsonResponse(data, safe=False)

#Historico Inventario
@login_required()
@permission_required('producto.view_inventario')
def list_ajustar_historial_inventario(request):
    return render(request, "ventas/producto/inventario/list_historial_ajuste.html")


def list_ajuste_inventario_historial_ajax(request):
    query = request.GET.get('busqueda')
    if query != "":
        inve = Inventario.objects.filter(Q(id_producto__id__icontains=query) | Q(id_producto__nombre_producto__icontains=query) | Q(id_producto__tipo_producto__nombre_tipo__icontains=query))
    else:
        inve = Inventario.objects.all()

    total = inve.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        page = math.ceil(start / length) + 1
        per_page = length

        inve = inve[start:start + length]

    data =[{'id': p.id_producto.id, 'nombre': p.id_producto.nombre_producto, 'descripcion': p.id_producto.descripcion, 'stock_total': p.stock_viejo,
            'stock_fisico': p.stock_fisico, 'diferencia': p.diferencia ,'fecha_ajuste': p.fecha_alta} for p in inve]        
    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response)


#Historico Producto
@login_required()
@permission_required('producto.view_inventario')
def list_historico_producto(request, id):
    context = {'id_producto': id}
    return render(request, "ventas/producto/list_historial_producto_precio.html", context)


def get_historico_producto(request, id):
    query = request.GET.get('busqueda')
    if query != "":
        productos = HistoricoProductoPrecio.objects.filter(id_producto=id)
        productos = productos.filter(Q(id_producto__nombre_producto__icontains=query) | Q(fecha_alta__icontains=query))
    else:
        productos = HistoricoProductoPrecio.objects.filter(id_producto=id)


    total = productos.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        page = math.ceil(start / length) + 1
        per_page = length

        productos = productos[start:start + length]

    data =[{'nombre': p.id_producto.nombre_producto, 'descripcion': p.id_producto.descripcion, 
            'precio_compra': p.precio_compra, 'fecha_compra': p.fecha_alta} for p in productos]        
        
    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response)

@csrf_exempt
def get_producto_antiparasitario(request):
    data = {}
    try:
        term = request.POST['term']
        if (request.POST['action'] == 'search_products'):
            data = []
            prods = Producto.objects.exclude(is_active='N').filter(nombre_producto__icontains=term)[0:10]
            for p in prods:
                item = p.obtener_dict()
                item['id'] = p.id
                producto_desc = '%s' % (p.nombre_producto)
                item['text'] = producto_desc
                data.append(item)    
    except Exception as e:
        data['error'] = str(e)
    return JsonResponse(data, safe=False)