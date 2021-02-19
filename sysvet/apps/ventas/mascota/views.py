from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Mascota, Especie, Raza
from .form import MascotaForm, EspecieForm

# Create your views here.
@login_required()
def add_mascota(request):
    form = MascotaForm
    if request.method == 'POST':
        form = MascotaForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('/mascota/list')
    context = {'form' : form}
    return render(request, 'mascota/add_mascota.html', context)

# Metodo para editar Mascotas
@login_required()
def edit_mascota(request, id):
    mascota = Mascota.objects.get(id=id)
    form = MascotaForm(instance=mascota)
    if request.method == 'POST':
        form = MascotaForm(request.POST, instance=mascota)
        if not form.has_changed():
            messages.info(request, "No ha hecho ningun cambio")
            return redirect('/mascota/list/')
        if form.is_valid():
            mascota = form.save(commit=False)
            mascota.save()
            messages.add_message(request, messages.SUCCESS, 'El Cliente se ha editado correctamente!')
            return redirect('/mascota/list/')

    context = {'form': form}
    return render(request, 'mascota/edit_mascota.html', context)    


@login_required()
def list_mascotas(request):
    mascotas = Mascota.objects.all()
    paginator = Paginator(mascotas, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj' : page_obj}
    return render(request, "mascota/list_mascotas.html", context)


    """
    Functions of Epecies 
    """
@login_required()
def add_especie(request):
    form = EspecieForm
    if request.method == 'POST':
        form = EspecieForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('/mascota/list')
    context = {'form' : form}
    return render(request, 'mascota/list_especie.html', context)


@login_required()
def list_especie(request):
    especie = Especie.objects.all()
    paginator = Paginator(especie, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj' : page_obj}
    return render(request, "mascota/list_especie.html", context)