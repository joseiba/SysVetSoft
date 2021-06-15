import json
from django.shortcuts import render
from django.http import JsonResponse

from apps.utiles.models import Timbrado, ProductoVendido
from apps.ventas.factura.models import FacturaCabeceraVenta, FacturaDetalleVenta
from apps.ventas.producto.models import Producto

# Create your views here.

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
    facturaVenta = FacturaCabeceraVenta.exclude(factura_anulada="S").all()
    try:
        if facturaVenta is not None:
            for fv in facturaVenta:
                facturaDetalle = FacturaDetalleVenta.objects.filter(id_factura_venta=fv.id)
                for factDet in facturaDetalle:
                    if factDet.tipo != 'S':
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
                            print(e)
    except Exception as e:
        print(e)
        pass
    
                