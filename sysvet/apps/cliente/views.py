from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import ClienteForm
from .views import Cliente

#Metodo para agregar cliente
@login_required()
def add_cliente(request):
    form = ClienteForm
    if request.method == 'POST':
        form = ClienteForm(request.POST or None)
        if form.is_valid():
            form.save:
            return redirect('/cliente/list')

    context = {'form' : form}
    return render(request, 'cliente/add_cliente.html', context)

