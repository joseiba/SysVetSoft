from django import forms
from  apps.ventas.factura.models import FacturaCabeceraVenta, FacturaDetalleVenta

class FacturaCabeceraVentaForm(forms.ModelForm):
    
    class Meta:
        model = FacturaCabeceraVenta
        exclude = ['is_active', 'estado']
        widgets = {
			'nro_factura': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off','name':'nro_factura','placeholder': 'Escriba el nro de factura','required':'required','onkeyup':'replaceABC(this)'}),
            'nro_timbrado': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off','name':'nro_factura','placeholder': 'Escriba el nro de timbrado','required':'required','onkeyup':'replaceABC(this)'}),
            'id_cliente' : forms.Select(attrs={'class':'form-control', 'id': 'cliente_select' ,'name':'id_cliente'}),
            'fecha_inicio_timbrado': forms.HiddenInput(),
            'fecha_fin_timbrado': forms.HiddenInput(),
            'ruc_empresa': forms.HiddenInput(),
		}


class FacturaDetalleVentaForm(forms.ModelForm):
    class Meta:
        model = FacturaDetalleVenta
        fields = ['cantidad']
        widgets = {
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'})
        }