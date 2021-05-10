from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
import math

from apps.compras.models import Proveedor, Pedido
from apps.compras.forms import ProveedorForm, PedidoForm
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
        try:
            pe = pro.id
            pedi = Pedido.objects.get(id_producto=pro.id)
            if pro.stock_minimo >= pro.stock:
                pedi.id_producto = pro
                pedi.save()
            else:
                pedi.delete()
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
    'cantidad': pe.cantidad_pedido, 'stock': pe.id_producto.stock} for pe in pedido]        

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