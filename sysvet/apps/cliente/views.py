from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import ClienteForm
from .models import Cliente, Ciudad


#Metodo para agregar cliente
@login_required()
def add_cliente(request):
    form = ClienteForm
    if request.method == 'POST':
        form = ClienteForm(request.POST or None)
        print(form.is_valid())
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
    print(cliente)
    form = ClienteForm(instance=cliente)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if not form.has_changed():
            return redirect('/cliente/list')
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.sace()
            return ('/cliente/list/')
    cuidad = Ciudad.objects.all()   
    context = {'form' : form, 'cuidad' : cuidad}
    return render(request, 'cliente/edit_cliente.html', context)



#Metodo para listar todos los clientes
@login_required()
def list_clientes(request):
    clientes = Cliente.objects.all()
    context = {'clientes' : clientes}
    return render(request, "cliente/list_cliente.html", context)



