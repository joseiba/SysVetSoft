from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import time, datetime
from django.db.models import Q
from django.contrib.auth.models import Group
import json

from apps.usuario.forms import FormLogin, UserForm, UserFormChange, GroupForm, GroupChangeForm
from apps.usuario.models import User


# Create your views here.

class Login(FormView):
    """[summary]

    Args:
        FormView ([Login]): [clase que ingresa al login]

    Returns:
        [Login]: [Retorna el index si esta autenticado o si no al login]
    """    
    template_name = 'registration/login.html'
    form_class = FormLogin
    success_url = reverse_lazy('index')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self,request,*args, **kwargs):    
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            if request.method == 'POST':
                username = request.POST['username']
                password = request.POST['password']
                usuario = authenticate(username=username, password=password)
                if usuario is None: 
                    messages.error(request,'El nombre de usuario y/o contraseña son incorrectos')         
            return super(Login, self).dispatch(request, *args, **kwargs)

    def form_valid(self,form):
        login(self.request,form.get_user())
        return super(Login,self).form_valid(form)

@login_required()
def logoutUser(request):
    """[summary]

    Args:
        request ([Logout]): [Metodo herado de logout de django para cerrar sesión]

    Returns:
        [Redirect template]: [Retorna el template del login]
    """    
    logout(request)
    return redirect('/accounts/login/')

@login_required()
def home_user(request):
    """[summary]

    Args:
        request ([Respuesta del index]): [Nombre de donde va ir redirigido]

    Returns:
        [Render template]: 
        [
            Se utiliza el metodo render, con los campos del request, y directorio
            de donde se encuentra el template            
        ]
    """    
    return render(request, "home/index.html")    


@login_required()
def list_usuarios(request):    
    return render(request, "usuario/list_usuarios.html")

@login_required()
def list_usuarios_ajax(request):
    query = request.GET.get('busqueda')
    if query != "":
        usuario = User.objects.exclude(is_active=False).filter(Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(username__icontains=query))
    else:
        usuario = User.objects.exclude(is_active=False).all()

    total = usuario.count()

    _start = request.GET.get('start')
    _length = request.GET.get('length')
    if _start and _length:
        start = int(_start)
        length = int(_length)
        page = math.ceil(start / length) + 1
        per_page = length

        usuario = usuario[start:start + length]

    data = [{'id': usu.id,'nombre': usu.first_name, 'apellido': usu.last_name, 'email': usu.email, 'username': usu.username} for usu in usuario]        
        
    response = {
        'data': data,
        'recordsTotal': total,
        'recordsFiltered': total,
    }
    return JsonResponse(response)

@login_required()
def add_usuario(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Se ha agregado correctamente!")
            return redirect('/usuario/add/')
        else:
            messages.error(request, form.errors)
    context = {'form': form}
    return render(request, 'usuario/add_usuario.html', context)

@login_required()
def edit_usuario(request, id):
    usuario = User.objects.get(id=id)
    form = UserFormChange(instance=usuario)
    if request.method == 'POST':
        form = UserFormChange(request.POST, instance=usuario)
        if not form.has_changed():
            messages.info(request, "No ha hecho ningun cambio")
            return redirect('/usuario/edit/' + str(id))
        if form.is_valid():
            form.save()
            # messages.success(request, "El cliente ha sido editado correctamente!")
            messages.add_message(request, messages.SUCCESS, 'Se ha editado correctamente!')
            return redirect('/usuario/edit/' + str(id))
        else:
            messages.error(request, form.errors)

    context = {'form': form, 'usuario': usuario}
    return render(request, 'usuario/edit_usuario.html', context)

#Roles
@login_required()
def add_rol(request):
    form = GroupForm()
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Se ha agregado correctamente!")
            return redirect('/usuario/addRol/')
        else:
            messages.error(request, form.errors)

    context = {'form': form,'groups': Group.objects.all()}
    return render(request, 'usuario/add_rol.html', context)


