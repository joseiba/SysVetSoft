from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator


from .forms import ClienteForm
from .models import Cliente, Ciudad


#Metodo para agregar cliente
@login_required()
def add_cliente(request):
    form = ClienteForm
    if request.method == 'POST':
        form = ClienteForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('/cliente/list')
    cuidad = Ciudad.objects.all()   
    context = {'form' : form, 'cuidad' : cuidad}
    return render(request, 'cliente/add_cliente.html', context)

# Metodo para editar Clientes
@login_required()
def edit_cliente(request, id):
    cliente = Cliente.objects.get(id=id)
    form = ClienteForm(instance=cliente)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if not form.has_changed():
            messages.info(request, "No ha hecho ningun cambio")
            return redirect('/cliente/list/')
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.save()
            messages.add_message(request, messages.SUCCESS, 'El Cliente se ha editado correctamente!')
            return redirect('/cliente/list/')

    context = {'form': form}
    return render(request, 'cliente/edit_cliente.html', context)

#Metodo para eliminar cliente
@login_required()
def delete_cliente(request, id):
    cliente = Cliente.objects.get(id=id)
    cliente.delete()
    return redirect('/cliente/list/')

#Metodo para listar todos los clientes
@login_required()
def list_clientes(request):
    clientes = Cliente.objects.all()
    paginator = Paginator(clientes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj' : page_obj}
    return render(request, "cliente/list_cliente.html", context)

#Metodo para la busqueda de clientes
@login_required()
def search_cliente(request):
    query = request.GET.get('q')
    if query:
        clientes = Cliente.objects.filter(Q(nombre_cliente__icontains=query) | Q(cedula__icontains=query))
    else:
        clientes = Cliente.objects.all()
    paginator = Paginator(clientes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = { 'page_obj': page_obj}
    return render(request, "cliente/list_cliente.html", context)


# def order_cliente(request):


