from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator


from .models import Mascota, Especie, Raza, Raza, FichaMedica, Vacuna, Consulta, Antiparasitario, HistoricoFichaMedica
from .form import MascotaForm, EspecieForm, RazaForm, FichaMedicaForm, VacunaForm, ConsultaForm, AntiparasitarioForm

import json

# Create your views here.
@login_required()
def add_mascota(request):
    form = MascotaForm    
    if request.method == 'POST':
        form = MascotaForm(request.POST, request.FILES) 
        if form.is_valid():           
            form.save()
            messages.success(request, 'Se ha agregado correctamente!')
            return redirect('/mascota/add')
    context = {'form' : form}
    return render(request, 'ventas/mascota/add_mascota.html', context)

# Metodo para editar Mascotas
@login_required()
def edit_mascota(request, id):
    mascota = Mascota.objects.get(id=id)
    form = MascotaForm(instance=mascota)
    if request.method == 'POST':
        form = MascotaForm(request.POST, request.FILES, instance=mascota)
        if not form.has_changed():
            messages.info(request, "No has hecho ningun cambio!")
            return redirect('/mascota/edit/' + str(id))
        if form.is_valid():
            mascota = form.save(commit=False)
            mascota.save()
            messages.success(request, 'Se ha editado correctamente!')
            return redirect('/mascota/edit/' + str(id))

    context = {'form': form, 'mascota': mascota}
    return render(request, 'ventas/mascota/edit_mascota.html', context)    


@login_required()
def list_mascotas(request):
    mascotas = Mascota.objects.all().order_by('-last_modified')
    paginator = Paginator(mascotas, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj' : page_obj}
    return render(request, "ventas/mascota/list_mascotas.html", context)

@login_required()
def search_mascota(request):
    query = request.GET.get('q')
    if query:
        mascota = Mascota.objects.filter(
            Q(nombre_mascota__icontains=query) | 
            Q(id_cliente__nombre_cliente__icontains=query) | 
            Q(id_cliente__apellido_cliente__icontains=query))
    else:
        mascota = Mascota.objects.all().order_by('-last_modified')
    paginator = Paginator(mascota, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = { 'page_obj': page_obj}
    return render(request, "ventas/mascota/list_mascotas.html", context)

@login_required()
def order_by_mascotas(request, id):
    print(id)
    if id == "1":
        print("funciona")
        mascota = Mascota.objects.all().order_by('nombre_mascota')
    else:
        mascota = Mascota.objects.all().order_by('peso')
    paginator = Paginator(mascota, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print(page_obj)
    context = { 'page_obj': page_obj}
    return render(request, "ventas/mascota/list_mascotas.html", context)

    """
    Functions of Epecies 
    """
@login_required()
def add_especie(request):
    form = EspecieForm
    if request.method == 'POST':
        form = EspecieForm(request.POST or None)
        if form.is_valid():
            messages.success(request, 'Se ha agregado correctamente!')
            form.save()
            return redirect('/mascota/listEspecie/')
    context = {'form' : form}
    return render(request, 'ventas/mascota/especie/add_especie_modal.html', context)


@login_required()
def edit_especie(request, id):
    especies = Especie.objects.get(id=id)
    form = EspecieForm(instance=especies)
    if request.method == 'POST':
        form = EspecieForm(request.POST, instance=especies)
        if not form.has_changed():
            messages.info(request, "No has hecho ningun cambio!")
            return redirect('/mascota/listEspecie/')
        if form.is_valid():
            especies = form.save(commit=False)
            especies.save()
            messages.success(request, 'Se ha editado correctamente!')
            return redirect('/mascota/listEspecie/')
    context = {'form' : form, 'especie': especies}
    return render(request, 'ventas/mascota/especie/edit_especie_modal.html', context)

@login_required()
def list_especie(request):
    especie = Especie.objects.all().order_by('-last_modified')
    paginator = Paginator(especie, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj' : page_obj}
    return render(request, "ventas/mascota/especie/list_especie.html", context)

@login_required()
def search_especie(request):
    query = request.GET.get('q')
    if query:
        especie = Especie.objects.filter(Q(nombre_especie__icontains=query))
    else:
        especie = Especie.objects.all().order_by('-last_modified')
    paginator = Paginator(especie, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = { 'page_obj': page_obj}
    return render(request, "ventas/mascota/especie/list_especie.html", context)

    """
    Functions of Razas
    """
@login_required()
def add_raza(request):
    form = RazaForm
    if request.method == 'POST':
        form = RazaForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Se ha agregado correctamente!')
            return redirect('/mascota/listRaza/')
    context = {'form' : form}
    return render(request, 'ventas/mascota/raza/add_raza_modal.html', context)

@login_required()
def edit_raza(request, id):
    raza = Raza.objects.get(id=id)
    form = RazaForm(instance=raza)
    if request.method == 'POST':
        form = RazaForm(request.POST, instance=raza)
        if not form.has_changed():
            messages.info(request, "No has hecho ningun cambio!")
            return redirect('/mascota/listRaza/')
        if form.is_valid():
            raza = form.save(commit=False)
            raza.save()
            messages.success(request, 'Se ha editado correctamente!')
            return redirect('/mascota/listRaza/')
    context = {'form' : form, 'raza': raza}
    return render(request, 'ventas/mascota/raza/edit_raza_modal.html', context)    

@login_required()
def list_raza(request):
    raza = Raza.objects.all().order_by('-last_modified')
    raza_especie = RazaForm
    paginator = Paginator(raza, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj' : page_obj, 'form': raza_especie}
    return render(request, "ventas/mascota/raza/list_raza.html", context)

@login_required()
def search_raza(request):
    query = request.GET.get('q')
    if query:
        raza = Raza.objects.filter(Q(nombre_raza__icontains=query))
    else:
        raza = Raza.objects.all().order_by('-last_modified')
    paginator = Paginator(raza, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = { 'page_obj': page_obj}
    return render(request, "ventas/mascota/raza/list_raza.html", context)    

#Funciones de Ficha Medicas
@login_required()
def edit_ficha_medica(request,id):
    mascota = Mascota.objects.get(id=id)
    fichaMedicaGet = FichaMedica.objects.get(id_mascota=id)
    vacunaGet = Vacuna.objects.get(id_ficha_medica=fichaMedicaGet.id)
    consultaGet = Consulta.objects.get(id_ficha_medica=fichaMedicaGet.id)
    antiparasitarioGet = Antiparasitario.objects.get(id_ficha_medica=fichaMedicaGet.id)
    historicoFichaMedica = HistoricoFichaMedica

    if request.method == 'POST':
        formFichaMedica = FichaMedicaForm(request.POST, instance=fichaMedicaGet)
        formVacuna = VacunaForm(request.POST, instance=vacunaGet)
        formConsulta = ConsultaForm(request.POST, instance=consultaGet)
        formAntiparasitario = AntiparasitarioForm(request.POST, instance=antiparasitarioGet)
        if not formVacuna.has_changed() and not formConsulta.has_changed() and not formAntiparasitario.has_changed():
            print(formVacuna.has_changed())
            print(formConsulta.has_changed())
            print(formAntiparasitario.has_changed())
            messages.info(request, "No has hecho ningun cambio!")
            return redirect('/mascota/editFichaMedica/' + str(id))   
        if formVacuna.is_valid() or formConsulta.is_valid() or formAntiparasitario.is_valid():                    
            consulta = formConsulta.save(commit=False)
            vacuna = formVacuna.save(commit=False)
            antiparasitario = formAntiparasitario.save(commit=False)
            fichaMedica = formFichaMedica.save(commit=False)
            fichaMedica.save()
            vacuna.save()
            antiparasitario.save()
            consulta.save()
            historicoFichaMedica = create_historico_ficha_medica(id)

            messages.success(request, 'Se ha editado correctamente!')
            return redirect('/mascota/editFichaMedica/' + str(id))

    formFichaMedica = FichaMedicaForm(instance=fichaMedicaGet)
    formVacuna = VacunaForm(instance=vacunaGet)
    formConsulta = ConsultaForm(instance=consultaGet)
    formAntiparasitario = AntiparasitarioForm(instance=antiparasitarioGet)

    context = {
        'mascota': mascota,
        'formFichaMedica': formFichaMedica,
        'formVacuna': formVacuna,
        'formConsulta': formConsulta,
        'formAntiparasitario': formAntiparasitario,
        'fichaMedicaGet': fichaMedicaGet,
    }

    return render(request, "ventas/mascota/ficha_medica/edit_ficha_medica.html", context)

#Historico de Ficha Medica
def list_historial(request, id):
    fichaMedicaGet = FichaMedica.objects.get(id_mascota=id)
    historico = HistoricoFichaMedica.objects.filter(id_ficha_medica=fichaMedicaGet.id).order_by('-last_modified')
    paginator = Paginator(historico, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj' : page_obj, 'historico': historico, 'id_mascota': id}

    return render(request, "ventas/mascota/ficha_medica/list_historico.html", context)


def create_historico_ficha_medica(id):
    historico = HistoricoFichaMedica()
    try:
        mascota = Mascota.objects.get(id=id)
        fichaMedicaGet = FichaMedica.objects.get(id_mascota=id)
        vacunaGet = Vacuna.objects.get(id_ficha_medica=fichaMedicaGet.id)
        consultaGet = Consulta.objects.get(id_ficha_medica=fichaMedicaGet.id)
        antiparasitarioGet = Antiparasitario.objects.get(id_ficha_medica=fichaMedicaGet.id)
        
        historico.vacuna = vacunaGet.vacuna
        historico.tipo_vacuna = vacunaGet.tipo_vacuna
        historico.proxima_vacunacion = vacunaGet.proxima_vacunacion
        historico.diagnostico = consultaGet.diagnostico
        historico.tratamiento = consultaGet.proximo_tratamiento
        historico.proximo_tratamiento = consultaGet.proximo_tratamiento
        historico.medicamento = consultaGet.medicamento
        historico.fecha_ultima_consulta = consultaGet.fecha_ultima_consulta
        historico.fecha_proxima_consulta = consultaGet.fecha_proxima_consulta
        historico.antiparasitario = antiparasitarioGet.antiparasitario
        historico.proximo_antiparasitario = antiparasitarioGet.proximo_antiparasitario
        historico.peso = mascota.peso
        historico.last_modified = fichaMedicaGet.fecha_create
        historico.id_ficha_medica = id
        historico.save()

        vacunaGet.vacuna = "-"
        vacunaGet.tipo_vacuna = "-"
        vacunaGet.proxima_vacunacion = "-"
        consultaGet.diagnostico = "-"
        consultaGet.tratamiento = "-"
        consultaGet.proximo_tratamiento = "-"
        consultaGet.medicamento = "-"
        consultaGet.fecha_ultima_consulta = None
        consultaGet.fecha_proxima_consulta = None
        antiparasitarioGet.antiparasitario = "-"
        antiparasitarioGet.proximo_antiparasitario = "-"
        formVacuna = VacunaForm(instance=vacunaGet)
        formConsulta = ConsultaForm(instance=consultaGet)
        formAntiparasitario = AntiparasitarioForm(instance=antiparasitarioGet)
        vacunaGet.save()
        consultaGet.save()
        antiparasitarioGet.save()

    except:
        pass

    return historico        






