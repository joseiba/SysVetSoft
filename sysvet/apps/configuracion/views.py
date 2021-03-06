from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
import math

from .models import Servicio, Empleado
from .forms import ServicioForm, EmpleadoForm

# Create your views here.
@login_required()
def add_servicio(request):
    form = ServicioForm    
    if request.method == 'POST':
        form = ServicioForm(request.POST) 
        if form.is_valid():           
            form.save()
            messages.success(request, 'Se ha agregado correctamente!')
            return redirect('/reserva/listServicio')
    context = {'form' : form}
    return render(request, 'reserva/servicio/add_servicio_modal.html', context)

@login_required()
def edit_servicio(request, id):
    servicios = Servicio.objects.get(id=id)
    form = ServicioForm(instance=servicios)
    if request.method == 'POST':
        form = ServicioForm(request.POST, instance=servicios)
        if not form.has_changed():
            messages.info(request, "No has hecho ningun cambio!")
            return redirect('/reserva/listServicio/')
        if form.is_valid():
            servicios = form.save(commit=False)
            servicios.save()
            messages.success(request, 'Se ha editado correctamente!')
            return redirect('/reserva/listServicio/')
    context = {'form' : form, 'servicios': servicios}
    return render(request, 'reserva/servicio/edit_servicio_modal.html', context)

@login_required()
def list_servicio(request):
    servicios = Servicio.objects.exclude(is_active="N").order_by('-last_modified')
    paginator = Paginator(servicios, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj' : page_obj}
    return render(request, "reserva/servicio/list_servicio.html", context)

@login_required()
def list_servicio_ajax(request):
    query = request.GET.get('busqueda')
    if query != "":
        servicios = Servicio.objects.exclude(is_active="N").filter(Q(nombre_servicio__icontains=query))
    else:
        servicios = Servicio.objects.exclude(is_active="N").order_by('-last_modified')

    total = servicios.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        page = math.ceil(start / length) + 1
        per_page = length

        clientes = clientes[start:start + length]

    data = [{'id': ser.id, 'nombre': ser.nombre_servicio, 'precio': ser.precio_servicio, 
        'cod_serv': ser.cod_serv } for ser in servicios]        

    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response)

#Metodo para eliminar servicio
@login_required()
def delete_servicio(request, id):
    servicio = Servicio.objects.get(id=id)
    if request.method == 'POST':
        servicio.is_active = "N"
        servicio.save()
        return redirect('/reserva/listServicio/')
    context = {'servicio': servicio}
    return render(request, "reserva/servicio/baja_servicio_modal.html", context)


@login_required()
def search_servicio(request):
    query = request.GET.get('q')
    if query:
        servicios = Servicio.objects.exclude(is_active="N").filter(Q(nombre_servicio__icontains=query))
    else:
        servicios = Servicio.objects.exclude(is_active="N").order_by('-last_modified')
    paginator = Paginator(servicios, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = { 'page_obj': page_obj}
    return render(request, "reserva/servicio/list_servicio.html", context)


#Empleados 
@login_required()
def add_empleado(request):
    form = EmpleadoForm    
    if request.method == 'POST':
        form = EmpleadoForm(request.POST) 
        if form.is_valid():           
            form.save()
            messages.success(request, 'Se ha agregado correctamente!')
            return redirect('/configuracion/listEmpleado/')
    context = {'form' : form}
    return render(request, 'configuraciones/empleado/add_empleado_modal.html', context)

@login_required()
def edit_empleado(request, id):
    emp = Empleado.objects.get(id=id)
    form = EmpleadoForm(instance=emp)
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=emp)
        if not form.has_changed():
            messages.info(request, "No has hecho ningun cambio!")
            return redirect('/configuracion/listEmpleado/')
        if form.is_valid():
            emp = form.save(commit=False)
            emp.save()
            messages.success(request, 'Se ha editado correctamente!')
            return redirect('/configuracion/listEmpleado/')
    context = {'form' : form, 'emp': emp}
    return render(request, 'configuraciones/empleado/edit_empleado_modal.html', context)


@login_required()
def list_empleado(request):
    emp = Empleado.objects.exclude(is_active="N").order_by('-last_modified')
    paginator = Paginator(emp, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj' : page_obj}
    return render(request, "configuraciones/empleado/list_empleados.html", context)

@login_required()
def get_list_empleados_ajax(request):
    query = request.GET.get('busqueda')
    if query != "":
        emp = Empleado.objects.exclude(is_active="N").filter(Q(nombre_emp__icontains=query) | Q(apellido_emp__icontains=query)
            | Q(ci_empe__icontains=query) | Q(id_servicio__nombre_servicio__icontains=query))
    else:
        emp = Empleado.objects.exclude(is_active="N").order_by('-last_modified')

    total = emp.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        page = math.ceil(start / length) + 1
        per_page = length

        emp = emp[start:start + length]

    data = [{'id': e.id, 'nombre': e.nombre_emp, 'apellido': e.apellido_emp, 'cedula': e.ci_empe, 'disponible': e.disponible,
        'nombre_servicio': e.id_servicio.nombre_servicio} for e in emp]        

    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response)

@login_required()
def delete_empleado(request, id):
    emp = Empleado.objects.get(id=id)
    if request.method == 'POST':
        emp.is_active = "N"
        emp.save()
        return redirect('/configuraciones/listEmpleados/')
    context = {'emp': emp}
    return render(request, "configuraciones/empleado/baja_empleado_modal.html", context)

@login_required()
def search_empleado(request):
    query = request.GET.get('q')
    if query:
        emp = Empleado.objects.exclude(is_active="N").filter(Q(nombre_emp__icontains=query))
    else:
        emp = Empleado.objects.exclude(is_active="N").order_by('-last_modified')
    paginator = Paginator(emp, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = { 'page_obj': page_obj}
    return render(request, "configuraciones/empleado/list_empleados.html", context)
