"""sysvet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_user
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from apps.usuario.views  import Login, logoutUser,home_user
from apps.cliente.views import add_cliente, list_clientes, edit_cliente, delete_cliente, search_cliente
from apps.mascota.views import list_mascotas

urlpatterns = [
    # app/ -> Genetelella UI and resources
    #path('app/', include('app.urls')),
    #path('', include('app.urls')),
    

    # Login and logout   
    path('admin/', admin.site.urls),
    path('', home_user, name="index"),
    path('accounts/login/', Login.as_view(), name='login'),
    path('logout/', logoutUser, name="logout"),

    #Urls clientes
    path('cliente/add/',add_cliente , name="add_cliente"),
    path('cliente/list/', list_clientes, name="list_cliente"),
    path('cliente/edit/<int:id>/', edit_cliente, name="edit_cliente"),
    path('<int:id>', delete_cliente, name="delete_cliente"),
    path('search/', search_cliente, name="search_cliente"),

    #Urls mascotas
    path('mascota/list/', list_mascotas , name="list_mascotas"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)