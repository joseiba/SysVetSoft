from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Servicio
from .forms import ServicioForm

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
    return render(request, 'reserva/servicios/edit_servicio_modal.html', context)

@login_required()
def list_servicio(request):
    servicios = Servicio.objects.exclude(is_active="N").order_by('-last_modified')
    paginator = Paginator(servicios, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj' : page_obj}
    return render(request, "reserva/servicio/list_servicio.html", context)

#Metodo para eliminar cliente
@login_required()
def delete_servicio(request, id):
    servicio = Servicio.objects.get(id=id)
    servicio.is_active = "N"
    servicio.save()
    return redirect('/reserva/listServicio/')

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
