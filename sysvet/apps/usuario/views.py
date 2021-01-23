from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


from .forms import FormLogin

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
            return super(Login, self).dispatch(request, *args, **kwargs)

    def form_valid(self,form):
        login(self.request,form.get_user())
        return super(Login,self).form_valid(form)

@login_required()
def logoutUser(request):
    logout(request)
    return redirect('/accounts/login/')

@login_required()
def home_user(request):
    return render(request, "base/index.html")    

