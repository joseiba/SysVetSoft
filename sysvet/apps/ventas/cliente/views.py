import json
import math
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.conf import settings
from io import BytesIO
from reportlab.pdfgen import canvas
from django.views.generic import View
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from django.http import JsonResponse

from .forms import ClienteForm
from .models import Cliente, Ciudad
from sysvet.settings import STATIC_URL, MEDIA_URL



#Metodo para agregar cliente
@login_required()
def add_cliente(request):
    form = ClienteForm
    if request.method == 'POST':
        form = ClienteForm(request.POST or None)
        if form.is_valid():
            messages.success(request, 'Se ha agregado correctamente!')
            form.save()
            return redirect('/cliente/add')
    cuidad = Ciudad.objects.all()   
    context = {'form' : form, 'cuidad' : cuidad}
    return render(request, 'ventas/cliente/add_cliente.html', context)

# Metodo para editar Clientes
@login_required()
def edit_cliente(request, id):
    cliente = Cliente.objects.get(id=id)
    form = ClienteForm(instance=cliente)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if not form.has_changed():
            messages.info(request, "No has hecho ningun cambio!")
            strId = str(id)
            return redirect('/cliente/edit/'+ strId)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.save()
            strId = str(id)
            messages.success(request, 'Se ha editado correctamente!')
            return redirect('/cliente/edit/'+ strId)

    context = {'form': form}
    return render(request, 'ventas/cliente/edit_cliente.html', context)

#Metodo para eliminar cliente
@login_required()
def delete_cliente(request, id):
    cliente = Cliente.objects.get(id=id)
    cliente.is_active = "N"
    cliente.save()
    return redirect('/cliente/list/')

#Metodo para listar todos los clientes
@login_required()
def list_clientes(request):    
    return render(request, "ventas/cliente/list_cliente.html")

@login_required()
def list_client_ajax(request):
    query = request.GET.get('busqueda')
    if query != "":
        clientes = Cliente.objects.exclude(is_active="N").filter(Q(nombre_cliente__icontains=query) | Q(cedula__icontains=query) | Q(id_ciudad__nombre_ciudad__icontains=query))
    else:
        clientes = Cliente.objects.exclude(is_active="N").order_by('-last_modified')

    total = clientes.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        page = math.ceil(start / length) + 1
        per_page = length

        clientes = clientes[start:start + length]

    data = [{'id': clie.id, 'nombre': clie.nombre_cliente, 'apellido': clie.apellido_cliente, 
        'cedula': clie.cedula, 'telefono': clie.telefono, 'direccion': clie.direccion, 'ciudad': clie.id_ciudad.nombre_ciudad } for clie in clientes]        
        
    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response)
    
#Metodo para la busqueda de clientes
@login_required()
def search_cliente(request):
    query = request.GET.get('q')
    if query:
        clientes = Cliente.objects.exclude(is_active="N").filter(Q(nombre_cliente__icontains=query) | Q(cedula__icontains=query) | Q(id_ciudad__nombre_ciudad__icontains=query))
    else:
        clientes = Cliente.objects.exclude(is_active="N").order_by('-last_modified')
    paginator = Paginator(clientes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = { 'page_obj': page_obj}
    return render(request, "ventas/cliente/list_cliente.html", context)

class ReporteClientesPDF(View):
    """def cabecera(self,pdf):
        #Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
        archivo_imagen = open('/sysvet/static/project_static/other/images/images.png', 'rb')
        #Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
        pdf.drawImage(archivo_imagen, 40, 750, 120, 90,preserveAspectRatio=True)"""  

    def get(self, request, *args, **kwargs):
        #Indicamos el tipo de contenido a devolver, en este caso un pdf
        response = HttpResponse(content_type='application/pdf')
        #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
        buffer = BytesIO()
        #Canvas nos permite hacer el reporte con coordenadas X y Y
        pdf = canvas.Canvas(buffer)
        #Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
        #self.cabecera(pdf)
        #Con show page hacemos un corte de página para pasar a la siguiente
        #Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
        pdf.setFont("Helvetica", 16)
        #Dibujamos una cadena en la ubicación X,Y especificada
        pdf.drawString(230, 790, u"SYS OHANA")
        pdf.setFont("Helvetica", 14)
        pdf.drawString(200, 770, u"REPORTE DE CLIENTES")
        y = 700
        self.tabla(pdf, y)

        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response    

    def tabla(self,pdf,y):
        #Creamos una tupla de encabezados para neustra tabla
        encabezados = ('Nombres', 'Apellidos', 'Cedula', 'Telefono', 'Dirección', 'Cuidad')
        #Creamos una lista de tuplas que van a contener a las personas
        detalles = [(cliente.nombre_cliente, cliente.nombre_cliente, cliente.cedula, cliente.telefono, cliente.direccion, cliente.id_ciudad.nombre_ciudad) for cliente in Cliente.objects.exclude(is_active="N").order_by('-last_modified')]
        #Establecemos el tamaño de cada una de las columnas de la tabla
        detalle_orden =  Table([encabezados] + detalles, colWidths=[3 * cm, 3 * cm, 2* cm, 3 * cm,6 * cm, 3 * cm])
        #Aplicamos estilos a las celdas de la tabla
        detalle_orden.setStyle(TableStyle(
            [
                #La primera fila(encabezados) va a estar centrada
                ('ALIGN',(0,0),(3,0),'CENTER'),
                #Los bordes de todas las celdas serán de color negro y con un grosor de 1
                ('GRID', (0, 0), (-1, -1), 1, colors.black), 
                #El tamaño de las letras de cada una de las celdas será de 10
                ('FONTSIZE', (0, 0), (-1, -1), 10),
            ]
        ))
        #Establecemos el tamaño de la hoja que ocupará la tabla 
        detalle_orden.wrapOn(pdf, 800, 600)
        #Definimos la coordenada donde se dibujará la tabla
        detalle_orden.drawOn(pdf, 10,y)


# def order_cliente(request):




