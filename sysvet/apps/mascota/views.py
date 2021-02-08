from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Mascota
from .form import MascotaForm

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


@login_required()
def list_mascotas(request):
    mascotas = Mascota.objects.all()
    paginator = Paginator(mascotas, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj' : page_obj}
    return render(request, "mascota/list_mascotas.html", context)
