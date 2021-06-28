import json
from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime, date

from apps.utiles.models import (Timbrado, ProductoVendido, ProductoComprados,ProductoVendidoMes, 
ProductoCompradoMes,ServicioVendido,GananciaPorMes, Cedula, Ruc)

from apps.ventas.factura.models import FacturaCabeceraVenta, FacturaDetalleVenta
from apps.compras.models import FacturaCompra, FacturaDet, Proveedor
from apps.ventas.producto.models import Producto
from apps.ventas.cliente.models import Cliente
from apps.ventas.mascota.models import Mascota
from apps.configuracion.models import Empleado, ConfiEmpresa
from apps.reserva.models import Reserva
from apps.ventas.mascota.models import HistoricoFichaMedica
from apps.usuario.models import User

hoy = date.today()
# Create your views here.
label_mes = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto',
            'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']


def reset_nro_timbrado(nro_timbrado):
    if nro_timbrado is not None:
        try:    
            factura = FacturaCabeceraVenta.objects.filter(nro_timbrado=nro_timbrado)
            if factura.count() > 0:
                nro_factura = factura.count() + 1
            else:
                nro_factura = 1
        except Exception as e:
            nro_factura = 1
    else:
        nro_factura = 1
    return nro_factura

def poner_vencido_timbrado(request):
    mensaje = ""
    try:
        timbrado = Timbrado.objects.get(nro_timbrado=request.GET.get('nro_timbrado'))
        timbrado.vencido = "S"
        timbrado.save()
        mensaje = "OK"
        response = {"mensaje": mensaje}
        return JsonResponse(response)
    except Exception as e:
        response = {"mensaje": "ERROR"}
        return JsonResponse(response)


def validate_nro_timbrado(request):
    mensaje = ""
    try:
        timbrado_vencido = Timbrado.objects.get(nro_timbrado=request.GET.get('nro_timbrado'))
        if timbrado_vencido.vencido == "S":
            mensaje = "OK"
        response = {"mensaje": mensaje}
        return JsonResponse(response)
    except Exception as e:
        response = {"mensaje": mensaje}
        return JsonResponse(response)


def cargar_productos_vendidos():
    facturaVenta = FacturaCabeceraVenta.objects.exclude(factura_anulada='S')
    try:
        if facturaVenta is not None:
            for fv in facturaVenta:
                facturaDetalle = FacturaDetalleVenta.objects.filter(id_factura_venta=fv.id)
                for factDet in facturaDetalle:
                    if factDet.tipo != 'S':
                        if factDet.detalle_cargado_reporte == 'N':
                            factDet.detalle_cargado_reporte = "S"
                            factDet.save()
                            try:
                                produc = ProductoVendido.objects.get(id_producto=factDet.id_producto.id)
                                produc.cantidad_vendida_total += factDet.cantidad
                                produc.save()
                            except Exception as e:
                                produc = ProductoVendido()
                                pro_id = Producto.objects.get(id=factDet.id_producto.id)
                                produc.id_producto = pro_id
                                produc.cantidad_vendida_total = factDet.cantidad
                                produc.save()
    except Exception as e:
        pass

def cargar_productos_comprados():
    facturaCompra = FacturaCompra.objects.all()
    try:
        if facturaCompra is not None:
            for fc in facturaCompra:
                facturaDetalle = FacturaDet.objects.filter(id_factura=fc.id)
                for factDet in facturaDetalle:
                    if factDet.detalle_cargado_reporte == 'N':
                        factDet.detalle_cargado_reporte = "S"
                        factDet.save()
                        try:
                            produc = ProductoComprados.objects.get(id_producto=factDet.id_producto.id)
                            produc.cantidad_comprada_total += factDet.cantidad
                            produc.save()
                        except Exception as e:
                            produc = ProductoComprados()
                            pro_id = Producto.objects.get(id=factDet.id_producto.id)
                            produc.id_producto = pro_id
                            produc.cantidad_comprada_total = factDet.cantidad
                            produc.save()
    except Exception as e:
        pass

def cargar_producto_vendido_mes():
    facturaVenta = FacturaCabeceraVenta.objects.exclude(factura_anulada='S')
    try:
        if facturaVenta is not None:
            for fv in facturaVenta:
                fecha_split = fv.fecha_alta.split('/')
                facturaDetalle = FacturaDetalleVenta.objects.filter(id_factura_venta=fv.id)
                for factDet in facturaDetalle:
                    if factDet.tipo != 'S':
                        if factDet.detalle_cargado_mes == 'N':
                            factDet.detalle_cargado_mes = "S"
                            factDet.save()
                            try:
                                produc = ProductoVendidoMes.objects.filter(anho=fecha_split[2])
                                if produc.count() == 0:
                                    produc = produc.get(anho=fecha_split[2])
                                produc = produc.get(numero_mes=int(fecha_split[1]))
                                produc.cantidad_vendida_total += factDet.cantidad
                                produc.save()
                            except Exception as e:
                                produc = ProductoVendidoMes()
                                pro_id = Producto.objects.get(id=factDet.id_producto.id)
                                produc.id_producto = pro_id
                                produc.label_mes = label_mes[int(fecha_split[1]) - 1]
                                produc.numero_mes = int(fecha_split[1])
                                produc.anho = fecha_split[2]
                                produc.cantidad_vendida_total = factDet.cantidad
                                produc.save()
    except Exception as e:
        pass

def cargar_productos_comprado_mes():
    facturaCompra = FacturaCompra.objects.all()
    try:
        if facturaCompra is not None:
            for fc in facturaCompra:
                fecha_split = fc.fecha_alta.split('/')
                facturaDetalle = FacturaDet.objects.filter(id_factura=fc.id)
                for factDet in facturaDetalle:
                    if factDet.detalle_cargado_mes == 'N':
                        factDet.detalle_cargado_mes = "S"
                        factDet.save()
                        try:
                            produc = ProductoCompradoMes.objects.filter(anho=fecha_split[2])
                            if produc.count() == 0:
                                produc = produc.get(anho=fecha_split[2])
                            produc = produc.get(numero_mes=int(fecha_split[1]))
                            produc.cantidad_comprada_total += factDet.cantidad
                            produc.save()
                        except Exception as e:
                            produc = ProductoCompradoMes()
                            pro_id = Producto.objects.get(id=factDet.id_producto.id)
                            produc.id_producto = pro_id
                            produc.label_mes = label_mes[int(fecha_split[1]) - 1]
                            produc.numero_mes = int(fecha_split[1])
                            produc.anho = fecha_split[2]
                            produc.cantidad_comprada_total = factDet.cantidad
                            produc.save()
    except Exception as e:
        pass

def cargar_servicios_vendidos():
    facturaVenta = FacturaCabeceraVenta.objects.exclude(factura_anulada='S')
    try:
        if facturaVenta is not None:
            for fv in facturaVenta:
                facturaDetalle = FacturaDetalleVenta.objects.filter(id_factura_venta=fv.id)
                for factDet in facturaDetalle:
                    if factDet.tipo != 'P':
                        if factDet.detalle_cargado_servicio == 'N':
                            factDet.detalle_cargado_servicio = "S"
                            factDet.save()
                            try:
                                produc = ServicioVendido.objects.get(id_producto=factDet.id_producto.id)
                                produc.cantidad_vendida_total += factDet.cantidad
                                produc.save()
                            except Exception as e:
                                produc = ServicioVendido()
                                pro_id = Producto.objects.get(id=factDet.id_producto.id)
                                produc.id_producto = pro_id
                                produc.cantidad_vendida_total = factDet.cantidad
                                produc.save()
    except Exception as e:
        pass


def cargar_ganacias_por_mes():
    facturaVenta = FacturaCabeceraVenta.objects.exclude(factura_anulada='S').all()

    try:
        for fv in facturaVenta:
            if fv.factura_to_reporte == 'N':
                fv.factura_to_reporte = 'S'
                fv.save()
                fecha_split = fv.fecha_alta.split('/')
                try:
                    reporte_ga = GananciaPorMes.objects.filter(anho=fecha_split[2])
                    if reporte_ga.count() == 0:
                        reporte_ga = reporte_ga.get(anho=fecha_split[2])
                    reporte_ga = reporte_ga.get(numero_mes=int(fecha_split[1]))
                    reporte_ga.total_mes += int(fv.total) 
                    reporte_ga.total_mes_formateado = "Gs. " + '{0:,}'.format(reporte_ga.total_mes)
                    reporte_ga.save()
                except Exception as e:
                    reporte_ga = GananciaPorMes()
                    reporte_ga.id_factura_venta = fv
                    reporte_ga.label_mes = label_mes[int(fecha_split[1]) - 1]
                    reporte_ga.numero_mes = int(fecha_split[1])
                    reporte_ga.anho = fecha_split[2]
                    reporte_ga.total_mes = int(fv.total)
                    reporte_ga.total_mes_formateado = "Gs. " + '{0:,}'.format(reporte_ga.total_mes)
                    reporte_ga.save()
    except Exception as e:
        pass


def validar_cedula(request):
    cedula = request.GET.get('cedula')
    mensaje = ""
    try:
        list_cedula = Cedula.objects.filter(nro_cedula=cedula)
        if Cliente.objects.filter(cedula=cedula).exists():
            mensaje = 'EX'
            response = {'mensaje': mensaje}
            return JsonResponse(response)
        elif Empleado.objects.filter(ci_empe=cedula).exists():
            mensaje = 'EX'
            response = {'mensaje': mensaje}
            return JsonResponse(response)
        else:
            mensaje = 'OK'
            response = {'mensaje': mensaje}
            return JsonResponse(response)
    except Exception as e:
        mensaje = 'ER'
        response = {'mensaje': mensaje}
        return JsonResponse(response)

def validar_ruc(request):
    obj_validar = request.GET.get('ruc')
    mensaje = ""
    try:
        list_validaciones = Ruc.objects.filter(nro_ruc=obj_validar)
        if Cliente.objects.filter(ruc=obj_validar).exists():
            mensaje = 'EX'
            response = {'mensaje': mensaje}
            return JsonResponse(response)
        elif Proveedor.objects.filter(ruc_proveedor=obj_validar).exists():
            mensaje = 'EX'
            response = {'mensaje': mensaje}
            return JsonResponse(response)
        elif ConfiEmpresa.objects.filter(ruc_empresa=obj_validar):
            mensaje = 'EX'
            response = {'mensaje': mensaje}
            return JsonResponse(response)
        else:
            mensaje = 'OK'
            response = {'mensaje': mensaje}
            return JsonResponse(response)
    except Exception as e:
        mensaje = 'ER'
        response = {'mensaje': mensaje}
        return JsonResponse(response)

def get_reserva_today(request):
    data = []
    try:
        fecha_hoy = date(hoy.year, hoy.month, hoy.day)
        reservas = Reserva.objects.filter(fecha_reserva=fecha_hoy)
        
        total =  reservas.count()

        _start = request.GET.get('start')
        _length = request.GET.get('length')
        if _start and _length:
            start = int(_start)
            length = int(_length)
            page = math.ceil(start / length) + 1
            per_page = length

            reservas = reservas[start:start + length]

        data =[{'cliente': r.id_cliente.nombre_cliente + ' ' + r.id_cliente.apellido_cliente,
                'mascota': r.id_mascota.nombre_mascota} for r in reservas]        
            
        response = {
            'data': data,
            'recordsTotal': total,
            'recordsFiltered': total,
        }
        return JsonResponse(response)
    except Exception as e:
        response = {
            'data': data,
            'recordsTotal': 0,
            'recordsFiltered': 0,
        }
        return JsonResponse(response)

def get_vacunas_today(request):
    data = []
    try:
        fecha_hoy = hoy.strftime("%d/%m/%Y")
        historico = HistoricoFichaMedica.objects.filter(fecha_proxima_aplicacion=fecha_hoy)
        
        total =  historico.count()

        _start = request.GET.get('start')
        _length = request.GET.get('length')
        if _start and _length:
            start = int(_start)
            length = int(_length)
            page = math.ceil(start / length) + 1
            per_page = length

            historico = historico[start:start + length]

        data =[{'cliente': h.id_mascota.id_cliente.nombre_cliente + ' ' + h.id_mascota.id_cliente.apellido_cliente,
                'mascota': r.id_mascota.nombre_mascota} for h in historico]        
            
        response = {
            'data': data,
            'recordsTotal': total,
            'recordsFiltered': total,
        }
        return JsonResponse(response)
    except Exception as e:
        response = {
            'data': data,
            'recordsTotal': 0,
            'recordsFiltered': 0,
        }
        return JsonResponse(response)

def total_user():
    try:
        usuario = User.objects.exclude(is_active=False).all()
        usuario = usuario.exclude(is_superuser=True)
        return usuario.count()
    except Exception as e:
        return 0

def total_cliente():
    try:
        cliente = Cliente.objects.exclude(is_active="N").all()
        return cliente.count()
    except Exception as e:
        return 0

def total_mascotas():
    try:
        mascotas = Mascota.objects.all()
        return mascotas.count()
    except Exception as e:
        return 0

def total_producto():
    try:
        productos = Producto.objects.exclude(is_active="N").all()        
        productos = productos.exclude(servicio_o_producto="S")
        productos = productos.exclude(producto_vencido="S")
        return productos.count()
    except Exception as e:
        return 0

def total_stock_minimo():
    prod_minimo = []
    try:
        productos = Producto.objects.exclude(is_active="N").order_by('-last_modified')
        productos = productos.exclude(servicio_o_producto="S")
        productos = productos.exclude(producto_vencido="S")

        for p in productos:
            if p.stock_minimo >= p.stock_total:
                prod_minimo.append(p)

        total =  len(prod_minimo)
        return total
    except Exception as e:
        return 0

def total_productos_a_vencer():
    prod_vencimiento = []
    try:
        confi = ConfiEmpresa.objects.get(id=1)
        dias_compare = confi.dias_a_vencer
    except Exception as e:
        dias_compare = 30
        
    try:
        productos = Producto.objects.exclude(is_active="N").order_by('-last_modified')
        productos = productos.exclude(servicio_o_producto="S")

        for p in productos:
            if p.fecha_vencimiento is not None:
                if rest_dates(p.fecha_vencimiento) <= dias_compare:
                    prod_vencimiento.append(p)

        total =  len(prod_vencimiento)
        return total
    except Exception as e:
        return 0

def total_vacunas_aplicadas():
    try:
        historico = HistoricoFichaMedica.objects.all()
        total =  historico.count()
        return total
    except Exception as e:
        return 0

def total_reservas_hoy():
    try:
        fecha_hoy = date(hoy.year, hoy.month, hoy.day)
        reservas = Reserva.objects.filter(fecha_reserva=fecha_hoy)
        total =  reservas.count()
        return total
    except Exception as e:
        return 0

def total_vacunas_proximas():
    try:
        confi = ConfiEmpresa.objects.get(id=1)
        dias_compare = confi.dias_alert_vacunas
    except Exception as e:
        dias_compare = 30
    
    try:
        list_historico = HistoricoFichaMedica.objects.all()
        for f in list_historico:
            if f.fecha_proxima_aplicacion is not None:
                if rest_dates(f.fecha_proxima_aplicacion) <= dias_compare:
                    ficha.append(f)

        total =  len(ficha)        
    except Exception as e:
        return 0


def rest_dates(fecha_vencimiento):
    try:
        fechaDate = date(hoy.year, hoy.month, hoy.day)
        fecha_vencimiento_split = fecha_vencimiento.split('/')          
        fecha_vencimiento_compare = date(int(fecha_vencimiento_split[2]), int(fecha_vencimiento_split[1]), int(fecha_vencimiento_split[0]))
        return (fecha_vencimiento_compare - hoy).days if (fecha_vencimiento_compare - hoy).days >= 0 else 0
    except Exception as e:
        return 0