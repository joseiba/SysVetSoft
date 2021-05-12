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

from apps.ventas.cliente.views import (add_cliente, list_clientes, edit_cliente, delete_cliente, search_cliente, ReporteClientesPDF,
list_client_ajax, list_client_ajax)

from apps.ventas.producto.views import add_tipo_producto, list_tipo_producto, edit_tipo_producto, search_tipo_producto, baja_tipo_producto, alta_tipo_producto, vence_si_no, add_deposito, list_deposito, edit_deposito, search_deposito, add_producto, edit_producto, list_producto, delete_producto, search_producto, mover_producto

from apps.ventas.mascota.views import (list_mascotas, add_mascota, edit_mascota, list_especie, add_especie, 
edit_especie,search_especie, list_raza, add_raza, edit_raza, search_raza,search_mascota, 
edit_ficha_medica, list_historial, list_especie_ajax, get_list_raza_ajax)

from apps.reserva.views import (add_reserva, edit_reserva, list_reserva, delete_reserva, search_reserva, 
validar_fecha_hora, get_mascota_cliente, get_min_service, get_mascota_selected)

from apps.configuracion.views import (add_servicio, edit_servicio, delete_servicio, list_servicio, search_servicio, 
add_empleado, edit_empleado, list_empleado, delete_empleado, search_empleado, list_servicio_ajax, get_list_empleados_ajax)

from apps.compras.views import (add_proveedor, edit_proveedor, list_proveedor_ajax, delete_proveedor, list_proveedor,
list_pedido, list_pedido_ajax, edit_pedido, list_facturas, list_facturas_ajax)

urlpatterns = [
    # Login and logout   
    path('admin/', admin.site.urls),
    path('', home_user, name="index"),
    path('accounts/login/', Login.as_view(), name='login'),
    path('logout/', logoutUser, name="logout"),

    #Urls clientes
    path('cliente/add/',add_cliente , name="add_cliente"),
    path('cliente/list/', list_clientes, name="list_cliente"),
    path('cliente/get_list_client/', list_client_ajax, name="list_client_ajax"),
    path('cliente/edit/<int:id>/', edit_cliente, name="edit_cliente"),
    path('<int:id>', delete_cliente, name="delete_cliente"),
    path('cliente/search/', search_cliente, name="search_cliente"),
    path('cliente/reportePDF', ReporteClientesPDF.as_view() , name="reporte_pdf_cliente"),


    #Urls tipo producto
    path('tipoProducto/add/',add_tipo_producto , name="add_tipo_producto"),
    path('tipoProducto/list/', list_tipo_producto, name="list_tipo_producto"),
    path('tipoProducto/edit/<int:id>/', edit_tipo_producto, name="edit_tipo_producto"),
    path('tipoProducto/baja/<int:id>/', baja_tipo_producto, name="baja_tipo_producto"),
    path('tipoProducto/alta/<int:id>/', alta_tipo_producto, name="alta_tipo_producto"),
    path('tipoProducto/search/', search_tipo_producto, name="search_tipo_producto"),
    path('tipoProducto/vence_si_no/', vence_si_no, name="vence_si_no"),

    #Urls producto
    path('producto/add/', add_producto, name="add_producto"),
    path('producto/list/', list_producto, name="list_producto"),
    path('producto/edit/<int:id>/', edit_producto, name="edit_producto"),
    path('producto/mover/<int:id>/', mover_producto, name="mover_producto"),
    path('producto/search/', search_producto, name="search_producto"),
    path('<int:id>', delete_producto, name="delete_producto"),


    #Urls deposito
    path('deposito/add/',add_deposito , name="add_deposito"),
    path('deposito/list/', list_deposito, name="list_deposito"),
    path('deposito/edit/<int:id>/', edit_deposito, name="edit_deposito"),
    path('deposito/search/', search_deposito, name="search_deposito"),

    #Urls mascotas
    path('mascota/list/', list_mascotas , name="list_mascotas"),     
    path('mascota/add/',  add_mascota, name="add_mascota"),
    path('mascota/edit/<int:id>/',edit_mascota , name="edit_mascota"),
    path('mascota/searchMascota/', search_mascota, name="search_mascota"),
    path('mascota/listEspecie/', list_especie , name="list_especie"),
    path('mascota/get_list_especie/', list_especie_ajax , name="list_especie_ajax"),
    path('mascota/addEspecie/',  add_especie, name="add_especie"),
    path('mascota/editEspecie/<int:id>/',  edit_especie, name="edit_especie"),
    path('mascota/searchEspecie/', search_especie, name="search_especie"),
    path('mascota/listRaza/', list_raza , name="list_raza"),
    path('mascota/get_list_raza/', get_list_raza_ajax , name="get_list_raza_ajax"),
    path('mascota/addRaza/',  add_raza, name="add_raza"),
    path('mascota/editRaza/<int:id>/',  edit_raza, name="edit_raza"),
    path('mascota/searchRaza/', search_raza, name="search_raza"),
    path('mascota/editFichaMedica/<int:id>/', edit_ficha_medica, name="edit_ficha_medica"),
    path('mascota/historial/<int:id>/', list_historial , name="list_historial"),    
    #End Urls Mascotas

    #Urls reservas 
    path('reserva/listServicio/', list_servicio , name="list_servicio"),
    path('reserva/addServicio/',  add_servicio, name="add_servicio"),
    path('reserva/editServicio/<int:id>/',edit_servicio , name="edit_servicio"),
    path('reserva/searchServicio/', search_servicio, name="search_servicio"),
    path('reserva/bajaServicio/<int:id>/', delete_servicio, name="delete_servicio"),
    path('reserva/listReserva/', list_reserva , name="list_reserva"),
    path('reserva/addReserva/',  add_reserva, name="add_reserva"),
    path('reserva/editReserva/<int:id>/',edit_reserva , name="edit_reserva"),
    path('reserva/bajaReserva/<int:id>/', delete_reserva, name="delete_reserva"),
    path('reserva/searchReserva/', search_reserva, name="search_reserva"),
    path('reserva/validarDatos/', validar_fecha_hora, name="search_reserva"),
    path('reserva/getMascotaCliente', get_mascota_cliente, name="get_mascota_cliente"),
    path('reserva/getTimeServices', get_min_service, name="get_min_service"),
    path('reserva/getMascotaSelected', get_mascota_selected, name="get_mascota_selected"),

    #Urls configuraciones 
    path('configuracion/listEmpleado/', list_empleado , name="list_empleado"),
    path('configuracion/get_list_servicio_ajax/', list_servicio_ajax , name="list_servicio_ajax"),
    path('configuracion/addEmpleado/',  add_empleado, name="add_empleado"),
    path('configuracion/editEmpleado/<int:id>/',edit_empleado , name="edit_empleado"),
    path('configuracion/searchEmpleado/', search_empleado, name="search_empleado"),
    path('configuracion/bajaEmpleado/<int:id>/', delete_empleado, name="delete_empleado"),
    path('configuracion/get_list_empleados_ajax/', get_list_empleados_ajax, name="get_list_empleados_ajax"),

    #Urls compras
    path('compra/addProveedor/', add_proveedor , name="add_proveedor"),
    path('compra/listProveedor/', list_proveedor, name="list_proveedor"),
    path('compra/get_list_proveedor/', list_proveedor_ajax, name="list_proveedor_ajax"),
    path('compra/editProveedor/<int:id>/', edit_proveedor, name="edit_proveedor"),
    path('compra/deleteProveedor/<int:id>/', delete_proveedor, name="delete_proveedor"),
    path('compra/listPedido/', list_pedido, name="list_pedido"),
    path('compra/get_list_pedido/', list_pedido_ajax, name="list_pedido_ajax"),
    path('compra/editPedido/<int:id>/', edit_pedido, name="edit_pedido"),
    path('compra/listFacturas/', list_facturas, name="list_facturas"),\
    path('compra/get_list_proveedor/', list_proveedor_ajax, name="list_proveedor_ajax"),
    path('compra/get_list_facturas/', list_facturas_ajax, name="list_facturas_ajax"),

    
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)