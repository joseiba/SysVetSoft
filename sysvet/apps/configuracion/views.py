from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
import math

from apps.configuracion.models import Servicio, Empleado, ConfiEmpresa, TipoVacuna
from apps.configuracion.forms import ServicioForm, EmpleadoForm, ConfiEmpresaForm, TipoVacunaForm
from apps.ventas.producto.models import Deposito
from apps.ventas.producto.models import Producto
from apps.utiles.models import Timbrado, Ruc, Cedula

# Create your views here.

#Configuraciones iniciales
@login_required()
@permission_required('configuracion.add_confiempresa')
def confi_inicial(request):
    try:
        confi = ConfiEmpresa.objects.get(id=1) 
        confiUbi = ConfiEmpresa.objects.get(id=1)    
        form = ConfiEmpresaForm(instance=confi)
        if request.method == 'POST':
            form = ConfiEmpresaForm(request.POST, instance=confi)
            if not form.has_changed():
                messages.info(request, "No has hecho ningun cambio!")
                return redirect('/configuracion/confiInicial/')
            if form.is_valid():
                confi = form.save(commit=False)
                timbrado = Timbrado()
                timbrado_existe = Timbrado.objects.filter(nro_timbrado= request.POST.get('nro_timbrado'))
                if timbrado_existe.count() == 0:
                    timbrado.nro_timbrado = request.POST.get('nro_timbrado')
                    timbrado.fecha_inicio_timbrado = request.POST.get('fecha_inicio_timbrado')
                    timbrado.fecha_fin_timbrado = request.POST.get('fecha_fin_timbrado')
                    timbrado.save()
                confi.save() 
                try:
                    depo = Deposito.objects.get(descripcion=confiUbi.ubicacion_deposito_inicial)   
                    depo.descripcion =  request.POST.get('ubicacion_deposito_inicial')     
                    depo.save()
                except:                                              
                    depo = Deposito()
                    depo.descripcion = request.POST.get('ubicacion_deposito_inicial')
                    depo.save()

                messages.success(request, 'Se ha agregado correctamente!')
                return redirect('/configuracion/confiInicial/')
    except Exception as e:
        print(e)
        pass
    context = {'form' : form}
    return render(request, 'configuraciones/generales/confi_inicial.html', context)   

#Servicios
@login_required()
@permission_required('configuracion.add_servicio')
def add_servicio(request):
    form = ServicioForm    
    if request.method == 'POST':
        form = ServicioForm(request.POST) 
        if form.is_valid():           
            ser = form.save(commit=False)
            ser.save()
            pro = Producto()
            pro.codigo_producto = request.POST.get("cod_serv")
            pro.nombre_producto = request.POST.get("nombre_servicio")
            pro.descripcion = request.POST.get("nombre_servicio")
            pro.precio_compra = request.POST.get("precio_servicio")
            pro.precio_venta = request.POST.get("precio_servicio")
            pro.stock_minimo = 0
            pro.stock = 1
            pro.servicio_o_producto = 'S'
            pro.id_servicio = ser.id
            pro.save()
            messages.success(request, 'Se ha agregado correctamente!')
            return redirect('/reserva/listServicio')
    context = {'form' : form}
    return render(request, 'reserva/servicio/add_servicio_modal.html', context)

@login_required()
@permission_required('configuracion.change_servicio')
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
            pro = Producto.objects.get(id_servicio=id)
            pro.codigo_producto = request.POST.get("cod_serv")
            pro.nombre_producto = request.POST.get("nombre_servicio")
            pro.descripcion = request.POST.get("nombre_servicio")
            pro.precio_compra = request.POST.get("precio_servicio")
            pro.precio_venta = request.POST.get("precio_servicio")
            pro.id_servicio = servicios.id
            pro.save()
            messages.success(request, 'Se ha editado correctamente!')
            return redirect('/reserva/listServicio/')
    context = {'form' : form, 'servicios': servicios}
    return render(request, 'reserva/servicio/edit_servicio_modal.html', context)

@login_required()
@permission_required('configuracion.view_servicio')
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

    data = [{'id': ser.id, 'nombre': ser.nombre_servicio, 'precio': ser.precio_servicio } for ser in servicios]        

    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response)

#Metodo para eliminar servicio
@login_required()
@permission_required('configuracion.delete_servicio')
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
@permission_required('configuracion.add_empleado')
def add_empleado(request):
    form = EmpleadoForm    
    if request.method == 'POST':
        form = EmpleadoForm(request.POST) 
        if form.is_valid():           
            form.save()
            messages.success(request, 'Se ha agregado correctamente!')
            cedula = Cedula()
            cedula.nro_cedula = request.POST.get('ci_empe')
            cedula.save()
            return redirect('/configuracion/listEmpleado/')
    context = {'form' : form}
    return render(request, 'configuraciones/empleado/add_empleado_modal.html', context)

@login_required()
@permission_required('configuracion.change_empleado')
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
            cedula = Cedula()
            cedula.nro_cedula = request.POST.get('ci_empe')
            cedula.save()
            messages.success(request, 'Se ha editado correctamente!')
            return redirect('/configuracion/listEmpleado/')
    context = {'form' : form, 'emp': emp}
    return render(request, 'configuraciones/empleado/edit_empleado_modal.html', context)


@login_required()
@permission_required('configuracion.view_empleado')
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
@permission_required('configuracion.delete_empleado')
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


@login_required()
@permission_required('configuracion.view_confiempresa')
def list_historial_timbrado(request):
    return render(request,"configuraciones/generales/list_historial_timbrado.html")

@login_required()
def get_historial_timbrado_ajax(request):
    query = request.GET.get('busqueda')
    if query != "":
        timbra = Timbrado.objects.filter(Q(nro_timbrado__icontains=query))
        timbra = timbra.order_by('id')
    else:
        timbra = Timbrado.objects.all().order_by('id')
        timbra = timbra.order_by('id')

    total = timbra.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        page = math.ceil(start / length) + 1
        per_page = length

        timbra = timbra[start:start + length]

    data = [{'id': t.id, 'nro_timbrado': t.nro_timbrado, 'fecha_inicio': t.fecha_inicio_timbrado,
            'fecha_fin': t.fecha_fin_timbrado, 'estado': t.vencido} for t in timbra]        

    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response)


#tipos de vacunas
@login_required()
@permission_required('configuracion.add_tipovacuna')
def add_vacuna(request):
    form = TipoVacunaForm
    if request.method == 'POST':
        form = TipoVacunaForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Se ha agregado correctamente!')
            return redirect('/configuracion/listVacunas')
    context = {'form' : form}
    return render(request, 'configuraciones/vacunas/add_tipo_vacunas.html', context)

@login_required()
@permission_required('configuracion.change_tipovacuna')
def edit_vacuna(request, id):
    vacu = TipoVacuna.objects.get(id=id)
    form = TipoVacunaForm(instance=vacu)
    if request.method == 'POST':
        form = TipoVacunaForm(request.POST, instance=vacu)
        if not form.has_changed():
            messages.info(request, "No has hecho ningun cambio!")
            return redirect('/configuracion/listVacunas')
        if form.is_valid():
            vacu = form.save(commit=False)
            vacu.save()
            messages.success(request, 'Se ha editado correctamente!')
            return redirect('/configuracion/listVacunas/')
    context = {'form' : form, 'vacu': vacu}
    return render(request, 'configuraciones/vacunas/edit_tipo_vacunas.html', context)    

@login_required()
@permission_required('configuracion.view_tipovacuna')
def list_vacunas(request):
    return render(request, "configuraciones/vacunas/list_tipos_vacunas.html")

@login_required()
def get_list_vacunas_ajax(request):
    query = request.GET.get('busqueda')
    if query != "":
        vacu = TipoVacuna.objects.filter(Q(nombre_vacuna__icontains=query))
    else:
        vacu = TipoVacuna.objects.all()

    total = vacu.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        page = math.ceil(start / length) + 1
        per_page = length

        vacu = vacu[start:start + length]

    data = [{'id': va.id, 'nombre_vacuna': va.nombre_vacuna, 'periodo': va.periodo_aplicacion } for va in vacu]        

    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response) 


def get_periodo_vacunacion(request):
    mensaje = ""
    try:
        vacuna = TipoVacuna.objects.get(id=request.GET.get("tipo"))
        response = {'mensaje': mensaje, 'periodo': vacuna.periodo_aplicacion}
        return JsonResponse(response) 
    except Exception as e:
        mensaje = "error"
        response = {'mensaje': mensaje}
        return JsonResponse(response) 
