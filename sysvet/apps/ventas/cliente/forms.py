from django import forms

from .models import Cliente

class ClienteForm(forms.ModelForm):
    """[summary]

    Args:
        forms ([ClienteForm]): [Formulario de cliente]
    """    
    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
			'nombre_cliente' : forms.TextInput(attrs={'class':'form-control','data-validate-length-range':'6', 
                'data-validate-words':'1', 'name': 'nombre_cliente', 'placeholder': 'Nombre del Cliente', 'required': 'required'}),
			'apellido_cliente' : forms.TextInput(attrs={'class':'form-control','data-validate-length-range':'6', 
                'data-validate-words':'1', 'name': 'apellido_cliente', 'placeholder': 'Apellido del Cliente', 'required': 'required'}),
			'direccion' : forms.TextInput(attrs={'class':'form-control','name': 'direccion', 'placeholder': 'Dirección', 'type':'text', 'required': 'required' }),
			'cedula' : forms.TextInput(attrs={'class':'form-control', 'name':'cedula', 'placeholder': 'Nro. Cédula', 'required':'required'}),
			'ruc' : forms.TextInput(attrs={'class':'form-control', 'name': 'ruc', 'placeholder': 'RUC', 'type':'text'}),
			'telefono' : forms.TextInput(attrs={'class':'form-control tel','placeholder': 'Telefono','type': 'tel', 'name':'telefono', 'required':'required',
                'data-validate-length-range': '9'}),
            'email' : forms.TextInput(attrs={'class':'form-control optional', 'placeholder': 'Email','name':'email', 'type':'email'}),
            'id_ciudad' : forms.Select(attrs={'class':'form-control', 'id': 'id_ciudad','required':'required' ,'name':'id_ciudad'})
		}