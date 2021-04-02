from django import forms

from .models import Cliente

class ClienteForm(forms.ModelForm):
    """[summary]

    Args:
        forms ([ClienteForm]): [Formulario de cliente]
    """    
    class Meta:
        model = Cliente
        exclude = ['is_active']
        widgets = {
			'nombre_cliente' : forms.TextInput(attrs={'class':'form-control','data-validate-length-range':'6', 
                'data-validate-words':'1', 'name': 'nombre_cliente', 'placeholder': 'Nombre del Cliente', 'required': 'required','onkeyup':'replaceCaratect(this)'}),
			'apellido_cliente' : forms.TextInput(attrs={'class':'form-control','data-validate-length-range':'6', 
                'data-validate-words':'1', 'name': 'apellido_cliente', 'placeholder': 'Apellido del Cliente', 'required': 'required','onkeyup':'replaceCaratect(this)'}),
			'direccion' : forms.TextInput(attrs={'class':'form-control','name': 'direccion', 'placeholder': 'Dirección','onkeyup':'replaceDirection(this)','type':'text', 'required': 'required'}),
			'cedula' : forms.TextInput(attrs={'class':'form-control', 'name':'cedula', 'placeholder': 'Nro. Cédula', 'required':'required','onkeyup':'replaceABC(this)'}),
			'ruc' : forms.TextInput(attrs={'class':'form-control', 'name': 'ruc', 'placeholder': 'RUC', 'type':'text','onkeyup':'replaceABC(this)'}),
			'telefono' : forms.TextInput(attrs={'class':'form-control tel','placeholder': 'Telefono','type': 'tel', 'name':'telefono', 'required':'required',
                'data-validate-length-range': '9','onkeyup':'replaceABC(this)'}),
            'email' : forms.TextInput(attrs={'class':'form-control optional', 'placeholder': 'Email','name':'email', 'type':'email', 'id':'email'}),
            'id_ciudad' : forms.Select(attrs={'class':'form-control', 'id': 'id_ciudad','required':'required' ,'name':'id_ciudad'})
		}