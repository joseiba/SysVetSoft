from django import forms

from .models import Servicio


class ServicioForm(forms.ModelForm):
    """[summary]

    Args:
        forms ([ServicioForm]): [Formulario de servicios]
    """    
    class Meta:
        model = Servicio
        exclude = ['is_active']
        widgets = {
            'cod_servicio' : forms.TextInput(attrs={'class':'form-control', 'name': 'cod_servicio', 'placeholder': 'Nombre del Servicio', 'required': 'required','onkeyup':'replaceCaratect(this)'}),
            'min_sev' : forms.TextInput(attrs={'class':'form-control', 'name': 'min_sev', 'placeholder': 'Nombre del Servicio', 'required': 'required','onkeyup':'replaceCaratect(this)'}),
			'nombre_servicio' : forms.TextInput(attrs={'class':'form-control','data-validate-length-range':'20', 
                'data-validate-words':'4', 'name': 'nombre_servicio', 'placeholder': 'Nombre del Servicio', 'required': 'required','onkeyup':'replaceCaratect(this)'}),
			'precio_servicio' : forms.TextInput(attrs={'class':'form-control', 'name': 'precio_servicio', 'placeholder': 'Precio del Servicio', 
                'required': 'required','onkeyup':'replaceABC(this)'}),
		}
