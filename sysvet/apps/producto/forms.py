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
			'nombre_tipo' : forms.TextInput(attrs={'class':'form-control','data-validate-length-range':'6', 
                'data-validate-words':'1', 'name': 'nombre_tipo', 'placeholder': 'Nombre Tipo Producto', 'required': 'required'}),
			'fecha_alta' : forms.TextInput(attrs={'class':'form-control','type':'date',
                'name': 'fecha_alta', 'placeholder': 'Fecha de Alta', 'readonly': 'readonly'}),
			'fecha_baja' : forms.TextInput(attrs={'class':'date-picker form-control','type':'datetime',
                'name': 'fecha_baja', 'placeholder': 'Fecha de Baja', 'onfocus':'this.type="date"', 'onmouseover':'this.type="date"', 
                'onclick':'this.type="date"', 'onblur':'this.type="text"', 'onmouseout':'timeFunctionLong(this)'}),
			
		}