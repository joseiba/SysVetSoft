from django import forms

from .models import TipoProducto

class TipoProductoForm(forms.ModelForm):
    """[summary]

    Args:
        forms ([TipoProductoForm]): [Formulario de tipo de producto]
    """    
    class Meta:
        model = TipoProducto
        fields = '__all__'
        widgets = {
			'nombre_tipo' : forms.TextInput(attrs={'class':'form-control','data-validate-length-range':'200', 'name': 'nombre_tipo', 'placeholder': 'Nombre Tipo Producto', 'required': 'required'}),
			'fecha_alta' : forms.TextInput(attrs={'class':'form-control','type':'date',
                'name': 'fecha_alta', 'placeholder': 'Fecha de Alta', 'readonly': 'readonly'}),
			'fecha_baja' : forms.TextInput(attrs={'class':'form-control','type':'datetime', 'name': 'fecha_baja', 
                'placeholder': 'Fecha de Baja', 'readonly': 'readonly'}),
			
		}