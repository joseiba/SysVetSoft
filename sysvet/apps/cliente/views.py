from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import ClienteForm
from .models import Cliente

#Metodo para agregar cliente
@login_required()
def add_cliente(request):
    form = ClienteForm
    if request.method == 'POST':
        form = ClienteForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('/cliente/list')

    context = {'form' : form}
    print("entro")
    return render(request, 'cliente/add_cliente.html', context)

#Metodo para listar todos los clientes
@login_required()
def list_clientes(request):
    clientes = Cliente.objects.all()
    context = {'clientes' : clientes}
    return render(request, "cliente/list_cliente.html", context)



