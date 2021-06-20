import json
from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime


from apps.utiles.models import (Timbrado, ProductoVendido, ProductoComprados,ProductoVendidoMes, 
ProductoCompradoMes,ServicioVendido,GananciaPorMes)

from apps.ventas.factura.models import FacturaCabeceraVenta, FacturaDetalleVenta
from apps.compras.models import FacturaCompra, FacturaDet
from apps.ventas.producto.models import Producto

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
                                produc = ProductoVendidoMes.objects.get(numero_mes=int(fecha_split[1]))
                                produc.cantidad_vendida_total += factDet.cantidad
                                produc.save()
                            except Exception as e:
                                produc = ProductoVendidoMes()
                                pro_id = Producto.objects.get(id=factDet.id_producto.id)
                                produc.id_producto = pro_id
                                produc.label_mes = label_mes[int(fecha_split[1]) - 1]
                                produc.numero_mes = int(fecha_split[1])
                                produc.cantidad_vendida_total = factDet.cantidad
                                produc.save()
                                print(e)
    except Exception as e:
        print(e)
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
                            produc = ProductoCompradoMes.objects.get(numero_mes=int(fecha_split[1]))
                            produc.cantidad_comprada_total += factDet.cantidad
                            produc.save()
                        except Exception as e:
                            produc = ProductoCompradoMes()
                            pro_id = Producto.objects.get(id=factDet.id_producto.id)
                            produc.id_producto = pro_id
                            produc.label_mes = label_mes[int(fecha_split[1]) - 1]
                            produc.numero_mes = int(fecha_split[1])
                            produc.cantidad_comprada_total = factDet.cantidad
                            produc.save()
    except Exception as e:
        print(e)
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
                    reporte_ga = GananciaPorMes.objects.get(numero_mes=int(fecha_split[1]))
                    reporte_ga.total_mes += int(fv.total) 
                    reporte_ga.total_mes_formateado = "Gs. " + '{0:,}'.format(reporte_ga.total_mes)
                    reporte_ga.save()
                except Exception as e:
                    print(e)
                    reporte_ga = GananciaPorMes()
                    reporte_ga.id_factura_venta = fv
                    reporte_ga.label_mes = label_mes[int(fecha_split[1]) - 1]
                    reporte_ga.numero_mes = int(fecha_split[1])
                    reporte_ga.total_mes = int(fv.total)
                    reporte_ga.total_mes_formateado = "Gs. " + '{0:,}'.format(reporte_ga.total_mes)
                    reporte_ga.save()
    except Exception as e:
        print(e)
        pass
