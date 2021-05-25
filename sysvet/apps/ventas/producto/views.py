from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from datetime import datetime

import json
from django.http import JsonResponse

from apps.ventas.producto.forms import TipoProductoForm, DepositoForm, ProductoForm
from apps.ventas.producto.models import TipoProducto, Deposito, Producto, ProductoStock
from apps.compras.models import FacturaCompra, FacturaDet
from apps.configuracion.models import ConfiEmpresa

date = datetime.now()

#Metodo para agregar tipo producto
@login_required()
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
def list_tipo_producto(request):
    tipos_productos = TipoProducto.objects.all()
    paginator = Paginator(tipos_productos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj' : page_obj}
    return render(request, "ventas/producto/list_tipo_producto.html", context)

#Metodo para la busqueda de tipo de producto
@login_required()
def search_tipo_producto(request):
    query = request.GET.get('q')
    if query:
        tipos_productos = TipoProducto.objects.filter(Q(nombre_tipo__icontains=query))
    else:
        tipos_productos = TipoProducto.objects.all()
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
def list_deposito(request):
    depositos = Deposito.objects.all()
    paginator = Paginator(depositos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj' : page_obj}
    return render(request, "ventas/producto/list_deposito.html", context)

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
def add_producto(request):
    form = ProductoForm
    try:
        confiEm = ConfiEmpresa.objects.get(id=1)
        depo = Deposito.objects.get(descripcion=confiEm.ubicacion_deposito_inicial)
        if request.method == 'POST':
            form = ProductoForm(request.POST or None)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, 'Producto agregado correctamente!')
                return redirect('/producto/add')  
    except:
        messages.add_message(request, messages.SUCCESS, 'Se debe agrega primeramente un deposito en configuraciones iniciales!')
        context = {'form' : form}
        return render(request, 'ventas/producto/add_producto.html', context)
    context = {'form' : form, 'deposito_inicial': depo.id}
    return render(request, 'ventas/producto/add_producto.html', context)

# Metodo para editar Productos
@login_required()
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
            producto.save()
            messages.add_message(request, messages.SUCCESS, 'El producto se ha editado correctamente!')
            return redirect('/producto/edit/' + str(id) )

    context = {'form': form, 'producto': producto}
    return render(request, 'ventas/producto/edit_producto.html', context)

# Metodo para editar Productos
@login_required()
def mover_producto(request, id):
    producto_movido = Producto()
    producto_moved = ProductoStock()
    producto = Producto.objects.get(id=id)
    form = ProductoForm(instance=producto)
    if request.method == 'POST':
        nombre_deposito = request.POST.get('id_deposito')
        cantidad = request.POST.get('stock')
        deposito = Deposito.objects.get(id=nombre_deposito)

        producto.stock = producto.stock - int(cantidad)
        producto.save() 

        producto_moved.producto_stock = int(cantidad)
        producto_moved.id_deposito = deposito
        producto_moved.id_producto = producto
        producto_moved.save()
        messages.add_message(request, messages.SUCCESS, 'El producto se ha movido correctamente!')

        return redirect('/producto/list/')

    context = {'form': form, 'producto': producto}
    return render(request, 'ventas/producto/mover_producto.html', context)

#Metodo para eliminar producto
@login_required()
def delete_producto(request, id):
    producto = Producto.objects.get(id=id)
    producto.is_active = "N"
    producto.save()
    return redirect('/producto/list/')

#Metodo para listar todos los productos
@login_required()
def list_producto(request):
    facturaCompra = FacturaCompra.objects.all()
    if facturaCompra is not None:
        for factCom in facturaCompra:
            if(factCom.factura_cargada_producto != 'S'):
                factCom.factura_cargada_producto = 'S'
                factCom.save()
                facDe = FacturaDet.objects.filter(id_factura=factCom)
                for factDet in facDe:
                    try:
                        prod = Producto.objects.get(id=factDet.id_pedido.id_producto.id)
                        prod.fecha_compra = factCom.fecha_emision
                        prod.precio_compra = factDet.id_pedido.id_producto.precio_compra
                        prod.stock = prod.stock + factDet.cantidad
                        prod.save()
                    except Exception as e:
                        pass
    producDetalle = ProductoStock.objects.all()
    productos = Producto.objects.exclude(is_active='N').order_by('-last_modified')
    paginator = Paginator(productos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj' : page_obj, 'producDetalle': producDetalle}
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

def mover_producto_detalle_general(request, id):
    try:
        pedido_trasladado = ProductoStock.objects.get(id=id)
        producto_general = Producto.objects.get(id=pedido_trasladado.id_producto.id)
        producto_general.stock = producto_general.stock + pedido_trasladado.producto_stock
        producto_general.save()
        pedido_trasladado.delete()
        messages.add_message(request, messages.SUCCESS, 'El producto se ha movido correctamente a la lista general!')
        return redirect('/producto/list/')
    except Exception as e:
        print(e)
        messages.add_message(request, messages.SUCCESS, 'ha ocurrido un error inesperado, intente más tarde!')        
        return redirect('/producto/list/')