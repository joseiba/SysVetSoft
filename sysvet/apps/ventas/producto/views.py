from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator

from .forms import TipoProductoForm
from .models import TipoProducto

from .forms import DepositoForm
from .models import Deposito


#Metodo para agregar tipo producto
@login_required()
def add_tipo_producto(request):
    form = TipoProductoForm
    if request.method == 'POST':
        form = TipoProductoForm(request.POST or None)
        if form.is_valid():
            form.save()
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

    context = {'form': form}
    return render(request, 'ventas/producto/edit_tipo_producto.html', context)


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


# def order_cliente(request):


#Metodo para agregar deposito
@login_required()
def add_deposito(request):
    form = DepositoForm
    if request.method == 'POST':
        form = DepositoForm(request.POST or None)
        if form.is_valid():
            form.save()
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

    context = {'form': form}
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

#Metodo para la busqueda de clientes
@login_required()
def search_deposito(request):
    query = request.GET.get('q')
    if query:
        depositos = Deposito.objects.filter(Q(descripcion__icontains=query))
    else:
        depositos = Deposito.objects.all()
    paginator = Paginator(depositos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = { 'page_obj': page_obj}
    return render(request, "ventas/producto/list_deposito.html", context)