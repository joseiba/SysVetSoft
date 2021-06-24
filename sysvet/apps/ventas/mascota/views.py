from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from datetime import date, datetime
import json
import math


from apps.ventas.mascota.models import Mascota, Especie, Raza, Raza, FichaMedica, Vacuna, Consulta, Antiparasitario, HistoricoFichaMedica
from .form import MascotaForm, EspecieForm, RazaForm, FichaMedicaForm, VacunaForm, ConsultaForm, AntiparasitarioForm
from apps.configuracion.models import TipoVacuna
from apps.ventas.producto.models import Producto

date = datetime.now()

# Create your views here.
@login_required()
@permission_required('mascota.add_mascota')
def add_mascota(request):
    form = MascotaForm    
    if request.method == 'POST':
        form = MascotaForm(request.POST, request.FILES)
        print(form)
        print(form.is_valid())
        if form.is_valid():           
            form.save()
            messages.success(request, 'Se ha agregado correctamente!')
            return redirect('/mascota/add')
    context = {'form' : form}
    return render(request, 'ventas/mascota/add_mascota.html', context)

# Metodo para editar Mascotas
@login_required()
@permission_required('mascota.view_mascota')
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
@permission_required('mascota.view_mascota')
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

    """
    Functions of Epecies 
    """
@login_required()
@permission_required('mascota.add_especie')
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
@permission_required('mascota.change_especie')
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
@permission_required('mascota.view_especie')
def list_especie(request):
    especie = Especie.objects.all().order_by('-last_modified')
    paginator = Paginator(especie, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj' : page_obj}
    return render(request, "ventas/mascota/especie/list_especie.html", context)

@login_required()
def list_especie_ajax(request):
    query = request.GET.get('busqueda')
    if query != "":
        especie = Especie.objects.filter(Q(nombre_especie__icontains=query))
    else:
        especie = Especie.objects.all().order_by('-last_modified')

    total = especie.count()


    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        page = math.ceil(start / length) + 1
        per_page = length

        especie = especie[start:start + length]

    data = [{'id': espe.id, 'nombre': espe.nombre_especie} for espe in especie]        

    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response)    

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
@permission_required('mascota.add_raza')
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
@permission_required('mascota.change_raza')
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
@permission_required('mascota.view_raza')
def list_raza(request):
    raza = Raza.objects.all().order_by('-last_modified')
    raza_especie = RazaForm
    paginator = Paginator(raza, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj' : page_obj, 'form': raza_especie}
    return render(request, "ventas/mascota/raza/list_raza.html", context)

@login_required()
def get_list_raza_ajax(request):
    query = request.GET.get('busqueda')
    if query != "":
        raza = Raza.objects.filter(Q(nombre_raza__icontains=query) | Q(id_especie__nombre_especie__icontains=query) )
    else:
        raza = Raza.objects.all().order_by('-last_modified')

    total = raza.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        page = math.ceil(start / length) + 1
        per_page = length

        raza = raza[start:start + length]

    data = [{'id': ra.id, 'nombre_raza': ra.nombre_raza, 'nombre_especie': ra.id_especie.nombre_especie } for ra in raza]        

    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response) 

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
@permission_required('mascota.view_mascota')
def edit_ficha_medica(request,id):
    mascota = Mascota.objects.get(id=id)
    fichaMedicaGet = FichaMedica.objects.get(id_mascota=id)
    vacunaGet = Vacuna.objects.get(id_ficha_medica=fichaMedicaGet.id)
    consultaGet = Consulta.objects.get(id_ficha_medica=fichaMedicaGet.id)
    antiparasitarioGet = Antiparasitario.objects.get(id_ficha_medica=fichaMedicaGet.id)
    historicoFichaMedica = HistoricoFichaMedica
    vacuna_aplicado = []
    vacuna_proxima = []
    vacunas = TipoVacuna.objects.all()
    try:    
        if request.method == 'POST':
            formFichaMedica = FichaMedicaForm(request.POST, instance=fichaMedicaGet)
            formVacuna = VacunaForm(request.POST, instance=vacunaGet)
            formConsulta = ConsultaForm(request.POST, instance=consultaGet)
            formAntiparasitario = AntiparasitarioForm(request.POST, instance=antiparasitarioGet)
            if not formVacuna.has_changed() and not formConsulta.has_changed() and not formAntiparasitario.has_changed():
                messages.info(request, "No has hecho ningun cambio!")
                return redirect('/mascota/editFichaMedica/' + str(id))   
            if formVacuna.is_valid() or formConsulta.is_valid() or formAntiparasitario.is_valid():
                proxima_vacuna = request.POST.get('proxima_vacunacion')   
                fecha_proxima_vacuna = request.POST.get('fecha_proxima_aplicacion')
                antiparasitario_aplicado = request.POST.get('antipara')
                proximo_antiparasitario_aplicado = request.POST.get('proximo_antipara')
                consulta = formConsulta.save(commit=False)
                vacuna = formVacuna.save(commit=False)
                antiparasitario = formAntiparasitario.save(commit=False)
                fichaMedica = formFichaMedica.save(commit=False)
                fichaMedica.save()
                vacuna.save()
                antiparasitario.save()
                consulta.save()
                historicoFichaMedica = create_historico_ficha_medica(id, proxima_vacuna, antiparasitario_aplicado, proximo_antiparasitario_aplicado)

                messages.success(request, 'Se ha editado correctamente!')
                return redirect('/mascota/editFichaMedica/' + str(id))
    except Exception as e:
        print(e)
        pass

    if vacunas.count() > 0:
        list_historico = HistoricoFichaMedica.objects.filter(id_ficha_medica=id)
        if list_historico.count() > 0:
            for vacu in vacunas:
                try:
                    vacu_historico = list_historico.get(vacuna=vacu)
                    if vacu.multi_aplicaciones == 'S':
                        vacuna_aplicado.append(vacu)
                        vacuna_proxima.append(vacu)
                except Exception as e:
                    vacuna_aplicado.append(vacu)
                    vacuna_proxima.append(vacu)
        else:
            for va in vacunas:
                vacuna_aplicado.append(va)
                vacuna_proxima.append(va)

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
        'vacunas_proxima': vacuna_proxima,
        'vacunas_aplicada': vacuna_aplicado
    }

    return render(request, "ventas/mascota/ficha_medica/edit_ficha_medica.html", context)

def get_prox_vacuna(request):
    vacuna_aplicada = TipoVacuna.objects.get(id=request.GET.get('id_vacuna'))
    list_vacunas = TipoVacuna.objects.filter(id_producto=vacuna_aplicada.id_producto)
    vacuna_proxima = []
    data = []
    list_historico = HistoricoFichaMedica.objects.filter(id_ficha_medica=request.GET.get('ficha_id'))
    if list_historico.count() > 0:
        try:
            if vacuna_aplicada.multi_aplicaciones == 'N':
                vacunas = list_vacunas.exclude(nombre_vacuna=vacuna_aplicada.nombre_vacuna)
            else:
                vacunas = list_vacunas
            for vacu in vacunas:
                try:
                    vacu_historico = list_historico.get(vacuna=vacu)
                    if vacu.multi_aplicaciones == 'S':
                        vacuna_proxima.append(vacu)
                except Exception as e:
                    vacuna_proxima.append(vacu)
        except Exception as e:
            for va in list_vacunas:
                vacuna_proxima.append(va)
    else:
        if vacuna_aplicada.multi_aplicaciones == 'N':
                vacunas = list_vacunas.exclude(nombre_vacuna=vacuna_aplicada.nombre_vacuna)
        else:
                vacunas = list_vacunas
        for va in vacunas:
            vacuna_proxima.append(va)

        for priodad_vacuna in list_vacunas:
            if int(priodad_vacuna.periodo_aplicacion) <= int(vacuna_aplicada.periodo_aplicacion):
                if priodad_vacuna.multi_aplicaciones == 'N':
                    try:
                        vacuna_proxima.remove(priodad_vacuna)
                    except:
                        pass

    data = [{'id': v.id, 'nombre_vacuna': v.nombre_vacuna } for v in vacuna_proxima]
    list_vacunas_proximas = json.dumps(data)
    response = {'proximas_vacunas': list_vacunas_proximas}
    return JsonResponse(response)

#Historico de Ficha Medica
def list_historial(request, id):
    fichaMedicaGet = FichaMedica.objects.get(id_mascota=id)
    historico = HistoricoFichaMedica.objects.filter(id_ficha_medica=fichaMedicaGet.id).order_by('-last_modified')
    paginator = Paginator(historico, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj' : page_obj, 'historico': historico, 'id_mascota': id}

    return render(request, "ventas/mascota/ficha_medica/list_historico.html", context)

def create_historico_ficha_medica(id, proxima_vacunacion, antiparasitario_aplicado, proximo_antiparasitario_aplicado):
    historico = HistoricoFichaMedica()
    try:
        historico_anteriores = HistoricoFichaMedica.objects.filter(id_ficha_medica=id)
        if historico_anteriores is not None:
            for hist in historico_anteriores:
                hist.fecha_proxima_aplicacion = None
                hist.save()
        if proxima_vacunacion != '-------':
            try:
                proxima_vacuna = TipoVacuna.objects.get(id=proxima_vacunacion)
            except Exception as e:
                pass
        mascota = Mascota.objects.get(id=id)
        fichaMedicaGet = FichaMedica.objects.get(id_mascota=id)
        vacunaGet = Vacuna.objects.get(id_ficha_medica=fichaMedicaGet.id)
        consultaGet = Consulta.objects.get(id_ficha_medica=fichaMedicaGet.id)
        antiparasitarioGet = Antiparasitario.objects.get(id_ficha_medica=fichaMedicaGet.id)

        if vacunaGet.id_vacuna is not None:
            producto = Producto.objects.get(id=vacunaGet.id_vacuna.id_producto.id)
            producto.stock_total = producto.stock_total - 1
            producto.stock = producto.stock - 1
            producto.save()

        historico.fecha_alta = date.strftime("%d/%m/%Y")
        historico.vacuna = vacunaGet.id_vacuna
        if proxima_vacunacion != '-------':
            historico.proxima_vacunacion = proxima_vacuna.nombre_vacuna
        else:
            historico.proxima_vacunacion = "-"

        if antiparasitario_aplicado != "Buscar":
            try:
                producto_anti = Producto.objects.get(id=antiparasitario_aplicado)
                producto_anti.stock_total = producto_anti.stock_total - 1
                producto_anti.stock = producto_anti.stock - 1
                producto_anti.save()
                anti_aplicado = producto_anti.nombre_producto
            except Exception as e:
                anti_aplicado = "-"
                pass
        else:
            anti_aplicado = "-"

        if proximo_antiparasitario_aplicado != "Buscar":
            try:
                producto_anti_proximo = Producto.objects.get(id=proximo_antiparasitario_aplicado)
                producto_anti_proximo.stock_total = producto_anti_proximo.stock_total - 1
                producto_anti_proximo.stock = producto_anti_proximo.stock - 1
                producto_anti_proximo.save()
                anti_proximo_aplicado = producto_anti_proximo.nombre_producto
            except Exception as e:
                anti_proximo_aplicado = "-"
                pass
        else:
            anti_proximo_aplicado = "-"

        historico.diagnostico = consultaGet.diagnostico
        historico.tratamiento = consultaGet.proximo_tratamiento
        historico.proximo_tratamiento = consultaGet.proximo_tratamiento
        historico.medicamento = consultaGet.medicamento
        historico.fecha_aplicacion = date.strftime("%d/%m/%Y")
        historico.fecha_proxima_aplicacion = vacunaGet.fecha_proxima_aplicacion
        historico.antiparasitario = anti_aplicado
        historico.proximo_antiparasitario = anti_proximo_aplicado
        historico.peso = mascota.peso
        historico.last_modified = fichaMedicaGet.fecha_create
        historico.id_ficha_medica = id
        historico.id_mascota = mascota
        historico.save()

        vacunaGet.id_vacuna = None
        vacunaGet.proxima_vacuna = "-"
        consultaGet.diagnostico = "-"
        consultaGet.tratamiento = "-"
        consultaGet.proximo_tratamiento = "-"
        consultaGet.medicamento = "-"
        vacunaGet.fecha_aplicacion = None
        vacunaGet.fecha_proxima_aplicacion = None
        antiparasitarioGet.antiparasitario = "-"
        antiparasitarioGet.proximo_antiparasitario = "-"
        formVacuna = VacunaForm(instance=vacunaGet)
        formConsulta = ConsultaForm(instance=consultaGet)
        formAntiparasitario = AntiparasitarioForm(instance=antiparasitarioGet)
        vacunaGet.save()
        consultaGet.save()
        antiparasitarioGet.save()

    except Exception as e:
        pass

    return historico        






