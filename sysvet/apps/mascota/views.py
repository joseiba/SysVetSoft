from django.shortcuts import render
from django.contrib.auth.decorators import login_required

array = ['hola', 'que', 'tal', 'estas', 'perro', 'gato']
# Create your views here.
@login_required()
def list_mascotas(request):
    form = array
    context = {'form':form}
    return render(request, "mascota/list_mascotas.html", context)
