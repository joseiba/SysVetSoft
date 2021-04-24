from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse


from .models import Reserva
from .forms import ReservaForm
from apps.configuracion.models import Servicio
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
    reserva.is_active = "N"
    reserva.save()
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
    print(hora)
    servicio = request.GET.get('servicio')
    cliente = request.GET.get('id_cliente')
    print("entro")

    messageReponse = ""
    reserva = Reserva.objects.filter(fecha_reserva=fecha, id_servicio=servicio)
    print("paso")
    if reserva is not None:
        print("entro 1 if")
        for re in reserva:
            if re.hora_reserva == hora:                
                messageReponse = "Ya existe un agendamiento para ese dia y para esa hora"
                response = { 'mensaje': messageReponse}
                return JsonResponse(response)
    response = { 'mensaje': messageReponse}
    return JsonResponse(response)