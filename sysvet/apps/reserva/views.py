from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from datetime import time, datetime
import json

from .models import Reserva
from .forms import ReservaForm
from apps.configuracion.models import Servicio, Empleado
from apps.configuracion.forms import ServicioForm
from apps.ventas.mascota.models import Mascota


hora_entrada = "08:00"
hora_salida_lun_vie = "18:00"
hora_salida_sab = "15:00"

#Reservas
@login_required()
def add_reserva(request):
    form = ReservaForm
    servicios = Servicio.objects.exclude(is_active="N").order_by('-last_modified')
    if request.method == 'POST':
        form = ReservaForm(request.POST) 
        if form.is_valid():           
            form.save()            
            messages.success(request, 'Se ha agregado correctamente!')
            return redirect('/reserva/listReserva/')
    context = {'form' : form}
    return render(request, 'reserva/add_reserva_modal.html', context)

@login_required()
def edit_reserva(request, id):
    reserva = Reserva.objects.get(id=id)
    form = ReservaForm(instance=reserva)
    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        if not form.has_changed():
            messages.info(request, "No has hecho ningun cambio!")
            return redirect('/reserva/listReserva/')
        if form.is_valid():
            reserva = form.save(commit=False)
            estado = request.POST.get('estado_re')
            if estado == 'FIN' or estado == 'CAN':
                reserva.disponible_emp = "S"                                                     
            reserva.save()
            messages.success(request, 'Se ha editado correctamente!')
            return redirect('/reserva/listReserva/')
    context = {'form' : form, 'reserva': reserva}
    return render(request, 'reserva/edit_reserva_modal.html', context)

@login_required()
def list_reserva(request):
    reserva = Reserva.objects.all()
    paginator = Paginator(reserva, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj' : page_obj}
    return render(request, "reserva/list_reserva.html", context)

#Metodo para eliminar servicio
@login_required()
def delete_reserva(request, id):
    reserva = Reserva.objects.get(id=id)
    reserva.delete()
    messages.success(request, 'La reserva se ha eliminado!')
    return redirect('/reserva/listReserva/')

@login_required()
def search_reserva(request):
    query = request.GET.get('q')
    if query:
        reserva = Reserva.objects.exclude(is_active="N").filter(Q(fecha_reserva__icontains=query))
    else:
        reserva = Reserva.objects.exclude(is_active="N").order_by('-last_modified')
    paginator = Paginator(reserva, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = { 'page_obj': page_obj}
    return render(request, "reserva/list_reserva.html", context)
        

def validar_fecha_hora(request):
    fecha = request.GET.get('fecha')
    hora = request.GET.get('hora')
    horaSelected = hora.split(':')
    servicio = request.GET.get('servicio')
    cliente = request.GET.get('id_cliente')
    mascota = request.GET.get('id_mascota')
    emp = request.GET.get('empleado')
    diaActual = datetime.now()
    mesActual =  str(diaActual.month) if diaActual.month > 9 else '0' + str(diaActual.month)
    dayActual = str(diaActual.day) if diaActual.day > 9 else '0' + str(diaActual.day)
    diaCompare = str(diaActual.year) + "-" + mesActual + "-" + dayActual
    messageReponse = ""
    isFalse = True
    isFalseOtherDay = True
    isFalseMascota = True    
    splitHoraActual = diaActual.hour
    serviEmpleado = Empleado.objects.filter(id_servicio=servicio).exclude(disponible=False)
    countEmpleadoServi = Empleado.objects.filter(id_servicio=servicio).exclude(disponible=False).count()
    countEmpleadoDiaServi = Reserva.objects.filter(id_servicio=servicio, fecha_reserva=fecha, hora_reserva=hora).exclude(disponible_emp='S').count()

    if diaCompare == fecha:
        if splitHoraActual <= int(horaSelected[0]):
            if countEmpleadoServi <= countEmpleadoDiaServi: 
                messageReponse = "Ya no hay disponibilidad del servicio para esa hora"
                response = { 'mensaje': messageReponse}
                return JsonResponse(response)
            else:
                try:
                    reserva = Reserva.objects.get(fecha_reserva=fecha, id_servicio=servicio, id_cliente=cliente, hora_reserva=hora, id_mascota=mascota, id_empleado=emp)
                except:
                    isFalse = False
                if isFalse:
                    messageReponse = "Este cliente ya tiene una reserva para ese dia y hora"
                    response = { 'mensaje': messageReponse}
                    return JsonResponse(response)                    
                try: 
                    reserva = Reserva.objects.get(fecha_reserva=fecha, hora_reserva=hora, id_mascota=mascota, id_empleado=emp)
                except: 
                    isFalseMascota = False
                    
                if isFalseMascota:
                    messageReponse = "Esta mascota ya tiene una reserva para este dia y hora"
                    response = { 'mensaje': messageReponse}
                    return JsonResponse(response)

        else:
            messageReponse = "Has seleccionado un horario que ya a ha pasado"
            response = { 'mensaje': messageReponse}
            return JsonResponse(response)
    else:
        if countEmpleadoServi <= countEmpleadoDiaServi:
            messageReponse = "Ya no hay disponibilidad del servicio para esa hora y dia"
            response = { 'mensaje': messageReponse}
            return JsonResponse(response)
        else:
            try:
                reserva = Reserva.objects.get(fecha_reserva=fecha, id_servicio=servicio, id_cliente=cliente, hora_reserva=hora, id_mascota=mascota, id_empleado=emp)
            except:
                isFalse = False
            if isFalse:
                messageReponse = "Este cliente ya tiene una reserva para ese dia y hora"
                response = { 'mensaje': messageReponse}
                return JsonResponse(response)
            try: 
                reserva = Reserva.objects.get(fecha_reserva=fecha, hora_reserva=hora, id_mascota=mascota, id_empleado=emp)
            except: 
                isFalseMascota = False

            if isFalseMascota:
                messageReponse = "Esta mascota ya tiene una reserva para este dia y hora"
                response = { 'mensaje': messageReponse}
                return JsonResponse(response)                                                      
    response = { 'mensaje': messageReponse}
    return JsonResponse(response)


def get_mascota_cliente(request):
    cliente = request.GET.get('id_cliente')

    mascotas = Mascota.objects.filter(id_cliente=cliente)

    listMascota = [{'id': mascota.id, 'nombre': mascota.nombre_mascota} for mascota in mascotas]

    listJsonMascotas = json.dumps(listMascota)
    if listJsonMascotas != '[]':
        response = { 'mascota': listJsonMascotas, 'mensaje': "Ok"}
        return JsonResponse(response)
    response = { 'mascota': listJsonMascotas, 'mensaje': ""}       
    return JsonResponse(response)

def get_min_service(request):
    servicio = request.GET.get('servicio')
    emp = Empleado.objects.filter(id_servicio=servicio)
    print("test")
    listEmpleado = [{'id': empleado.id, 'nombre': empleado.nombre_emp + " " + empleado.apellido_emp} for empleado in emp]
    print("test1")

    listJsonEmpleado= json.dumps(listEmpleado)
    isFalse = True
    try:
        minService = Servicio.objects.get(id=servicio)
    except:
        isFalse = False
    if isFalse:
        response = { 'tiempo': minService.min_serv, 'mensaje': "Ok", 'empleado': listJsonEmpleado}
        return JsonResponse(response)
    response = { 'tiempo': minService.min_serv, 'mensaje': "", 'empleado': listJsonEmpleado}       
    return JsonResponse(response)

def get_mascota_selected(request):
    cliente = request.GET.get('id_cliente')
    hora_reserva = request.GET.get('hora_reserva')
    fecha_reserva = request.GET.get('fecha_reserva')
    servicio = request.GET.get('servicio')
    emp = Empleado.objects.filter(id_servicio=servicio)
    mascotas = Mascota.objects.filter(id_cliente=cliente)
    listMascota = [{'id': mascota.id, 'nombre': mascota.nombre_mascota} for mascota in mascotas]
    listEmpleado = [{'id': empleado.id, 'nombre': empleado.nombre_emp + " " + empleado.apellido_emp} for empleado in emp]

    listJsonEmpleado= json.dumps(listEmpleado)
    listJsonMascotas = json.dumps(listMascota)
    reserva = Reserva.objects.get(fecha_reserva=fecha_reserva, id_servicio=servicio, id_cliente=cliente, hora_reserva=hora_reserva)
    if listJsonMascotas != '[]':
        response = { 'mascota': listJsonMascotas, 'mensaje': "Ok", 'mascota_selected': reserva.id_mascota.id, 'empleado': reserva.id_empleado.id, 'empleados':listJsonEmpleado}
        return JsonResponse(response)
    response = { 'mascota': listJsonMascotas, 'mensaje': ""}       
    return JsonResponse(response)


