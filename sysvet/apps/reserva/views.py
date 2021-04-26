from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from datetime import time, datetime

from .models import Reserva
from .forms import ReservaForm
from apps.configuracion.models import Servicio, Empleado
from apps.configuracion.forms import ServicioForm

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
    reserva = Reserva.objects.exclude(is_active="N").order_by('-last_modified')
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
    diaActual = datetime.now()
    mesActual =  str(diaActual.month) if diaActual.month > 9 else '0' + str(diaActual.month)
    dayActual = str(diaActual.day) if diaActual.day > 9 else '0' + str(diaActual.day)
    diaCompare = str(diaActual.year) + "-" + mesActual + "-" + dayActual
    print(diaCompare)
    messageReponse = ""
    isFalse = True
    splitHoraActual = diaActual.hour
    serviEmpleado = Empleado.objects.filter(id_servicio=servicio).exclude(disponible=False)
    countEmpleadoServi = Empleado.objects.filter(id_servicio=servicio).exclude(disponible=False).count()
    countEmpleadoDiaServi = Reserva.objects.filter(id_servicio=servicio, fecha_reserva=fecha, hora_reserva=hora).exclude(disponible_emp='S').count()

    if diaCompare == fecha:
        print('today')
        if splitHoraActual <= int(horaSelected[0]):
            print("hora")             
            if countEmpleadoServi <= countEmpleadoDiaServi: 
                messageReponse = "Ya no hay disponibilidad del servicio para esa hora"
                response = { 'mensaje': messageReponse}
                return JsonResponse(response)
            else:
                try:
                    reserva = Reserva.objects.get(fecha_reserva=fecha, id_servicio=servicio, id_cliente=cliente, hora_reserva=hora)
                except: 
                    isFalse = False
                if isFalse:
                    messageReponse = "Este cliente ya tiene una reserva para ese dia y hora"
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
                reserva = Reserva.objects.get(fecha_reserva=fecha, id_servicio=servicio, id_cliente=cliente, hora_reserva=hora)
            except: 
                isFalse = False
            if isFalse:
                messageReponse = "Este cliente ya tiene una reserva para ese dia y hora"
                response = { 'mensaje': messageReponse}
                return JsonResponse(response)   
    response = { 'mensaje': messageReponse}
    return JsonResponse(response)