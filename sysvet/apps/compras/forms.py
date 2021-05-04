from django import forms
from  apps.compras.models import Proveedor

class ProveedorForm(forms.ModelForm):
    """[summary]

    Args:
        forms ([ClienteForm]): [Formulario de cliente]
    """    
    class Meta:
        model = Proveedor
        exclude = ['is_active']
        widgets = {
			'nombre_proveedor' : forms.TextInput(attrs={'class':'form-control','name': 'nombre_proveedor', 'placeholder': 'Nombre del Proveedor', 'required': 'required','onkeyup':'replaceCaratect(this)'}),		
			'direccion' : forms.TextInput(attrs={'class':'form-control','name': 'direccion', 'placeholder': 'Dirección','onkeyup':'replaceDirection(this)','type':'text', 'required': 'required'}),
			'cedula' : forms.TextInput(attrs={'class':'form-control', 'name':'cedula', 'placeholder': 'Nro. Cédula', 'required':'required','onkeyup':'replaceABC(this)'}),
			'ruc_proveedor' : forms.TextInput(attrs={'class':'form-control', 'name': 'ruc_proveedor', 'placeholder': 'RUC', 'required': 'required','type':'text','onkeyup':'replaceABC(this)'}),
			'telefono' : forms.TextInput(attrs={'class':'form-control tel','placeholder': 'Telefono','type': 'tel', 'name':'telefono', 'required':'required',
                'data-validate-length-range': '9','onkeyup':'replaceABC(this)'}),
            'email' : forms.TextInput(attrs={'class':'form-control optional', 'placeholder': 'Email','name':'email', 'type':'email', 'id':'email'}),
		}