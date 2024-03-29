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

from apps.ventas.cliente.views import (add_cliente, list_clientes, edit_cliente, delete_cliente, search_cliente, 
ReporteClientesPDF, list_client_ajax, list_client_ajax, list_clientes_baja, get_client_baja, alta_cliente)

from apps.ventas.producto.views import (add_tipo_producto, list_tipo_producto, edit_tipo_producto, search_tipo_producto, 
baja_tipo_producto, alta_tipo_producto, vence_si_no, add_deposito, list_deposito, edit_deposito, search_deposito, 
add_producto, edit_producto, list_producto, delete_producto, search_producto, mover_producto, mover_producto_detalle_general,
list_productos_general, list_producto_general_ajax, get_list_deposito, get_list_tipo_producto, list_producto_vencido_ajax,
list_ajuste_inventario_ajax, list_ajustar_inventario, add_ajuste_inventario, list_ajuste_inventario_historial_ajax,
list_ajustar_historial_inventario, get_producto_antiparasitario, get_producto_inventario, list_historico_producto,
get_historico_producto)

from apps.ventas.mascota.views import (list_mascotas, add_mascota, edit_mascota, list_especie, add_especie, 
edit_especie,search_especie, list_raza, add_raza, edit_raza, search_raza,search_mascota, 
edit_ficha_medica, list_historial, list_especie_ajax, get_list_raza_ajax, get_prox_vacuna,get_list_historico_vacunas_aplicadas,
get_list_historico_vacunas_proximas)

from apps.reserva.views import (add_reserva, edit_reserva, list_reserva, delete_reserva, search_reserva, 
validar_fecha_hora, get_mascota_cliente, get_min_service, get_mascota_selected)

from apps.configuracion.views import (add_servicio, edit_servicio, delete_servicio, list_servicio, search_servicio, 
add_empleado, edit_empleado, list_empleado, delete_empleado, search_empleado, list_servicio_ajax, get_list_empleados_ajax,
confi_inicial, list_historial_timbrado, get_historial_timbrado_ajax, add_vacuna, edit_vacuna, list_vacunas, 
get_list_vacunas_ajax, get_periodo_vacunacion, add_ciudad, edit_ciudad, list_ciudades, get_list_ciudades)

from apps.compras.views import (add_proveedor, edit_proveedor, list_proveedor_ajax, delete_proveedor, list_proveedor,
list_pedido, list_pedido_ajax, edit_pedido, list_factura_compra, list_facturas_ajax, add_factura_compra, 
search_pediddos_factura, edit_factura_compra, list_pedido_compra, list_pedido_compra_ajax, add_pedido_compra, edit_pedido_compra,
reporte_compra_pdf, agregar_factura_compra)

from apps.ventas.factura.views import (list_factura_ventas, list_facturas__ventas_ajax, add_factura_venta, 
get_producto_servicio_factura, edit_factura_venta, anular_factura_venta, list_facturas_anuladas_ventas_ajax,
ver_factura_anulada_venta, validate_producto_stock, list_facturas_ventas_anuladas, reporte_factura_venta_pdf)

from apps.usuario.views import (list_usuarios, list_usuarios_ajax, add_usuario, edit_usuario, add_rol, get_group_list, 
change_password, edit_rol, delete_rol, baja_usuario, list_usuarios_baja_ajax, alta_usuario, list_usuarios_baja)

from apps.caja.views import (list_caja_ajax, list_cajas, add_caja, cerrar_caja, get_list_caja_historico, list_historico_caja, 
reporte_caja_pdf)

from apps.reporte.views import (reporte_producto,reporte_producto_comprados,reporte_ganancias_mes, reporte_prod_comprado, 
reporte_prod_vendido, reporte_productos_vendido_mes, get_producto_vendido_mes, reporte_productos_comprado_mes,
get_producto_comprado_mes, get_ganancias_mes, reporte_stock_minimo, get_producto_minimo, reporte_stock_a_vencer,
get_producto_vencimiento, reporte_servicio_vendido, get_servicio_vendido, list_proximas_vacunas, get_proximas_vacunas,
get_rango_mes_recaudacion, get_rango_mes_pro_comprado, get_rango_mes_pro_vendido, reporte_get_vacunas_aplicada,
reporte_vacunas_aplicadas)

from apps.utiles.views import (poner_vencido_timbrado, validate_nro_timbrado, validar_cedula, validar_ruc,
get_reserva_today, get_vacunas_today)

urlpatterns = [
    # Login and logout   
    path('SuperAdminUserDev/', admin.site.urls),
    path('', home_user, name="index"),
    path('accounts/login/', Login.as_view(), name='login'),
    path('logout/', logoutUser, name="logout"),

    #Usuarios
    path('usuario/listUsuarios/', list_usuarios, name="list_usuarios"),
    path('usuario/list_usuarios_ajax/', list_usuarios_ajax, name="list_usuarios_ajax"),
    path('usuario/list_usuarios_baja_ajax/', list_usuarios_baja_ajax, name="list_usuarios_baja_ajax"),
    path('usuario/add/', add_usuario , name="add_usuario"),
    path('usuario/edit/<int:id>/', edit_usuario, name="edit_usuario"),
    path('usuario/darBajaUsuario/<int:id>/', baja_usuario, name="baja_usuario"),
    path('usuario/altaUsuarios/<int:id>/', alta_usuario, name="alta_usuario"),
    path('usuario/addRol/', add_rol , name="add_rol"),
    path('usuario/editRol/<int:id>/', edit_rol , name="edit_rol"),
    path('usuario/eliminarRol/<int:id>/', delete_rol , name="delete_rol"),
    path('usuario/get_group_list/', get_group_list , name="get_group_list"),
    path('usuario/editPassword/<int:id>/', change_password , name="change_password"),
    path('usuario/listUsuariosBaja/', list_usuarios_baja, name="list_usuarios_baja"),

    #Urls clientes
    path('cliente/add/',add_cliente , name="add_cliente"),
    path('cliente/list/', list_clientes, name="list_cliente"),
    path('cliente/get_list_client/', list_client_ajax, name="list_client_ajax"),
    path('cliente/edit/<int:id>/', edit_cliente, name="edit_cliente"),
    path('<int:id>', delete_cliente, name="delete_cliente"),
    path('cliente/search/', search_cliente, name="search_cliente"),
    path('cliente/reportePDF', ReporteClientesPDF.as_view() , name="reporte_pdf_cliente"),
    path('cliente/altaCliente/<int:id>/',alta_cliente , name="alta_cliente"),
    path('cliente/listClientesBajas/', list_clientes_baja, name="list_clientes_baja"),
    path('cliente/get_client_baja/', get_client_baja, name="get_client_baja"),

    #Urls tipo producto
    path('tipoProducto/add/',add_tipo_producto , name="add_tipo_producto"),
    path('tipoProducto/list/', list_tipo_producto, name="list_tipo_producto"),
    path('tipoProducto/edit/<int:id>/', edit_tipo_producto, name="edit_tipo_producto"),
    path('tipoProducto/baja/<int:id>/', baja_tipo_producto, name="baja_tipo_producto"),
    path('tipoProducto/alta/<int:id>/', alta_tipo_producto, name="alta_tipo_producto"),
    path('tipoProducto/search/', search_tipo_producto, name="search_tipo_producto"),
    path('tipoProducto/vence_si_no/', vence_si_no, name="vence_si_no"),
    path('tipoProducto/get_list_tipo_producto/', get_list_tipo_producto, name="get_list_tipo_producto"),

    #Urls producto
    path('producto/add/', add_producto, name="add_producto"),
    path('producto/listDetalle/<int:id>/', list_producto, name="list_producto"),
    path('producto/listGeneral/', list_productos_general, name="list_productos_general"),
    path('producto/list_general_ajax/', list_producto_general_ajax, name="list_producto_general_ajax"),
    path('producto/list_producto_vencido_ajax/', list_producto_vencido_ajax, name="list_producto_vencido_ajax"),
    path('producto/edit/<int:id>/', edit_producto, name="edit_producto"),
    path('producto/mover/<int:id>/', mover_producto, name="mover_producto"),
    path('producto/search/', search_producto, name="search_producto"),
    path('producto/darBaja/<int:id>', delete_producto, name="delete_producto"),
    path('producto/moverGeneral/<int:id>/', mover_producto_detalle_general, name="mover_producto_detalle_general"),
    path('producto/list_ajuste_inventario_ajax/', list_ajuste_inventario_ajax, name="list_ajuste_inventario_ajax"),
    path('producto/list_ajustar_inventario/', list_ajustar_inventario, name="list_ajustar_inventario"),
    path('producto/addAjusteInventario/', add_ajuste_inventario, name="add_ajuste_inventario"),
    path('producto/list_ajuste_inventario_historial_ajax/', list_ajuste_inventario_historial_ajax, name="list_ajuste_inventario_historial_ajax"),
    path('producto/list_ajustar_historial_inventario/', list_ajustar_historial_inventario, name="list_ajustar_historial_inventario"),
    path('producto/get_producto_inventario/', get_producto_inventario, name="get_producto_inventario"),
    path('producto/get_producto_antiparasitario/', get_producto_antiparasitario, name="get_producto_antiparasitario"),
    path('producto/listHistoricoCompra/<int:id>/', list_historico_producto, name="list_historico_producto"),
    path('producto/get_historico_producto/<int:id>/', get_historico_producto, name="get_historico_producto"),


    #Urls deposito
    path('deposito/add/',add_deposito , name="add_deposito"),
    path('deposito/list/', list_deposito, name="list_deposito"),
    path('deposito/get_list_deposito/', get_list_deposito, name="get_list_deposito"),
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
    path('mascota/get_prox_vacuna/', get_prox_vacuna, name="get_prox_vacuna"),
    path('mascota/get_list_historico_vacunas_aplicadas/', get_list_historico_vacunas_aplicadas, name="get_list_historico_vacunas_aplicadas"),
    path('mascota/get_list_historico_vacunas_proximas/', get_list_historico_vacunas_proximas, name="get_list_historico_vacunas_proximas"),
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
    path('configuracion/confiInicial/', confi_inicial, name="confi_inicial"),
    path('configuracion/listHistorialTimbrado/', list_historial_timbrado , name="list_historial_timbrado"),
    path('configuracion/get_historial_timbrado_ajax/', get_historial_timbrado_ajax , name="get_historial_timbrado_ajax"),
    path('configuracion/listVacunas/', list_vacunas , name="list_vacunas"),
    path('configuracion/get_list_vacunas_ajax/', get_list_vacunas_ajax , name="get_list_vacunas_ajax"),
    path('configuracion/addVacuna/',  add_vacuna, name="add_vacuna"),
    path('configuracion/editVacuna/<int:id>/', edit_vacuna , name="edit_vacuna"),
    path('configuracion/get_periodo_vacunacion/', get_periodo_vacunacion , name="get_periodo_vacunacion"),
    path('configuracion/listCiudades/', list_ciudades , name="list_ciudades"),
    path('configuracion/get_list_ciudades/', get_list_ciudades , name="get_list_ciudades"),
    path('configuracion/addCiudad/',  add_ciudad, name="add_ciudad"),
    path('configuracion/editCiudad/<int:id>/',edit_ciudad , name="edit_ciudad"),



    #Urls compras
    path('compra/addProveedor/', add_proveedor , name="add_proveedor"),
    path('compra/listProveedor/', list_proveedor, name="list_proveedor"),
    path('compra/get_list_proveedor/', list_proveedor_ajax, name="list_proveedor_ajax"),
    path('compra/editProveedor/<int:id>/', edit_proveedor, name="edit_proveedor"),
    path('compra/deleteProveedor/<int:id>/', delete_proveedor, name="delete_proveedor"),
    path('compra/listPedido/', list_pedido, name="list_pedido"),
    path('compra/get_list_pedido/', list_pedido_ajax, name="list_pedido_ajax"),
    path('compra/editPedido/<int:id>/', edit_pedido, name="edit_pedido"),
    path('compra/listFacturasCompras/', list_factura_compra, name="list_factura_compra"),
    path('compra/addFacturaCompra/', agregar_factura_compra, name="add_factura_compra"),
    path('compra/editFacturaCompra/<int:id>/', edit_factura_compra, name="edit_factura_compra"),
    path('compra/get_list_proveedor/', list_proveedor_ajax, name="list_proveedor_ajax"),
    path('compra/get_list_facturas/', list_facturas_ajax, name="list_facturas_ajax"),
    path('compra/get_pedido_factura/', search_pediddos_factura, name="search_pediddos_factura"),
    path('compra/listPedidosCompra/', list_pedido_compra, name="list_pedido_compra"),
    path('compra/list_pedido_compra_ajax/', list_pedido_compra_ajax, name="list_pedido_compra_ajax"),
    path('compra/addPedidoCompra/', add_pedido_compra, name="add_pedido_compra"),
    path('compra/editPedidoCompra/<int:id>/', edit_pedido_compra, name="edit_pedido_compra"),
    path('compra/reporteCompra/<int:id>/', reporte_compra_pdf, name="reporte_compra_pdf"),

    #Ventas/Facturas
    path('factura/listFacturasVentas/', list_factura_ventas, name="list_factura_ventas"),
    path('factura/get_list_facturas_ventas/', list_facturas__ventas_ajax, name="list_facturas__ventas_ajax"),
    path('factura/addFacturaVenta/', add_factura_venta , name="add_factura_venta"),
    path('factura/get_producto_servicio_factura/', get_producto_servicio_factura, name="get_producto_servicio_factura"),
    path('factura/editFacturaVenta/<int:id>/', edit_factura_venta, name="edit_factura_venta"),
    path('factura/anularFacturaVenta/<int:id>/', anular_factura_venta, name="anular_factura_venta"),
    path('factura/get_list_facturas_anulas_ventas/', list_facturas_anuladas_ventas_ajax, name="list_facturas_anuladas_ventas_ajax"),
    path('factura/verDetalleFacturaAnulada/<int:id>/', ver_factura_anulada_venta, name="ver_factura_anulada_venta"),
    path('factura/validate_producto_stock/', validate_producto_stock , name="validate_producto_stock"),
    path('factura/listFacturasVentasAnuladas/', list_facturas_ventas_anuladas, name="list_facturas_ventas_anuladas"),
    path('factura/reporteFactura/<int:id>/', reporte_factura_venta_pdf, name="reporte_factura_venta_pdf"),

    #Caja
    path('caja/listCajas/', list_cajas, name="list_cajas"),
    path('caja/get_list_caja/', list_caja_ajax, name="list_caja_ajax"),
    path('caja/add/',add_caja , name="add_caja"),
    path('caja/cerrar_caja/<int:id>/',cerrar_caja , name="cerrar_caja"),
    path('caja/listHistoricoCajas/', list_historico_caja, name="list_historico_caja"),
    path('caja/get_list_caja_historico/', get_list_caja_historico, name="get_list_caja_historico"),
    path('caja/reporteCaja/<int:id>/', reporte_caja_pdf, name="reporte_caja_pdf"),

    #Caja
    path('reporte/listReporteProductoVendidos/', reporte_producto, name="reporte_producto"),
    path('reporte/listReporteProductosComprados/', reporte_producto_comprados, name="reporte_producto_comprados"),
    path('reporte/listReporteGanancias/', reporte_ganancias_mes, name="reporte_ganancias_mes"),
    path('reporte/get_productos_vendidos/', reporte_prod_vendido, name="reporte_prod_vendido"),
    path('reporte/get_productos_comprados/', reporte_prod_comprado, name="reporte_prod_comprado"),
    path('reporte/listProductosVendidoMes/', reporte_productos_vendido_mes, name="reporte_productos_vendido_mes"),
    path('reporte/get_productos_vendido_mes/', get_producto_vendido_mes, name="get_producto_vendido_mes"),
    path('reporte/listProductosCompradoMes/', reporte_productos_comprado_mes, name="reporte_productos_comprado_mes"),
    path('reporte/get_productos_comprado_mes/', get_producto_comprado_mes, name="get_producto_comprado_mes"),
    path('reporte/get_ganacias_mes/',get_ganancias_mes, name="get_ganancias_mes"),
    path('reporte/get_rango_mes/',get_rango_mes_recaudacion, name="get_rango_mes_recaudacion"),
    path('reporte/listProductosMinimos/', reporte_stock_minimo, name="reporte_stock_minimo"),
    path('reporte/get_producto_minimo/',get_producto_minimo, name="get_producto_minimo"),
    path('reporte/listProductosVencimiento/', reporte_stock_a_vencer, name="reporte_stock_a_vencer"),
    path('reporte/get_producto_vencimiento/',get_producto_vencimiento, name="get_producto_vencimiento"),
    path('reporte/listServiciosVendidos/', reporte_servicio_vendido, name="reporte_servicio_vendido"),
    path('reporte/get_servicio_vendido/',get_servicio_vendido, name="get_servicio_vendido"),
    path('reporte/listProximasVacunaciones/', list_proximas_vacunas, name="list_proximas_vacunas"),
    path('reporte/get_proximas_vacunas/',get_proximas_vacunas, name="get_proximas_vacunas"),
    path('reporte/get_rango_mes_pro_vendido/',get_rango_mes_pro_vendido, name="get_rango_mes_pro_vendido"),
    path('reporte/get_rango_mes_pro_comprado/',get_rango_mes_pro_comprado, name="get_rango_mes_pro_comprado"),
    path('reporte/listVacunasAplicadas/', reporte_vacunas_aplicadas, name="reporte_vacunas_aplicadas"),
    path('reporte/get_vacunas_aplicadas/', reporte_get_vacunas_aplicada, name="reporte_get_vacunas_aplicada"),

    #Utiles
    path('utiles/poner_vencido_timbrado/', poner_vencido_timbrado, name="poner_vencido_timbrado"),
    path('utiles/validate_nro_timbrado/', validate_nro_timbrado, name="validate_nro_timbrado"),
    path('utiles/validar_cedula/', validar_cedula, name="validar_cedula"),
    path('utiles/validar_ruc/', validar_ruc, name="validar_ruc"),
    path('utiles/get_reserva_today/', get_reserva_today , name="get_reserva_today"),
    path('utiles/get_vacunas_today/', get_vacunas_today , name="get_vacunas_today"),  


]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)