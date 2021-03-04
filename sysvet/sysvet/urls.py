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
from apps.ventas.producto.views import add_tipo_producto, list_tipo_producto, edit_tipo_producto, search_tipo_producto
from apps.ventas.cliente.views import add_cliente, list_clientes, edit_cliente, delete_cliente, search_cliente
from apps.ventas.mascota.views import (list_mascotas, add_mascota, edit_mascota, list_especie, add_especie, 
edit_especie,search_especie, list_raza, add_raza, edit_raza, search_raza,search_mascota, order_by_mascotas)

urlpatterns = [
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
    path('cliente/search/', search_cliente, name="search_cliente"),

    #Urls tipo producto
    path('tipoProducto/add/',add_tipo_producto , name="add_tipo_producto"),
    path('tipoProducto/list/', list_tipo_producto, name="list_tipo_producto"),
    path('tipoProducto/edit/<int:id>/', edit_tipo_producto, name="edit_tipo_producto"),
    path('tipoProducto/search/', search_tipo_producto, name="search_tipo_producto"),

    #Urls mascotas
    path('mascota/list/', list_mascotas , name="list_mascotas"),
    path('mascota/add/',  add_mascota, name="add_mascota"),
    path('mascota/edit/<int:id>/',edit_mascota , name="edit_mascota"),
    path('mascota/searchMascota/', search_mascota, name="search_mascota"),
    path('mascota/order_mascota/<int:id>/',  order_by_mascotas, name="order_by_mascotas"),
    path('mascota/listEspecie/', list_especie , name="list_especie"),
    path('mascota/addEspecie/',  add_especie, name="add_especie"),
    path('mascota/editEspecie/<int:id>/',  edit_especie, name="edit_especie"),
    path('mascota/searchEspecie/', search_especie, name="search_especie"),
    path('mascota/listRaza/', list_raza , name="list_raza"),
    path('mascota/addRaza/',  add_raza, name="add_raza"),
    path('mascota/editRaza/<int:id>/',  edit_raza, name="edit_raza"),
    path('mascota/searchRaza/', search_raza, name="search_raza"),
    #End Urls Mascotas
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)