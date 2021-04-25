from django import forms

from .models import Servicio, Empleado


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


class EmpleadoForm(forms.ModelForm):
    """[summary]

    Args:
        forms ([ServicioForm]): [Formulario de servicios]
    """    
    class Meta:
        model = Empleado
        exclude = ['is_active']
        widgets = {
            'nombre_emp' : forms.TextInput(attrs={'class':'form-control', 'name': 'nombre_emp', 'placeholder': 'Nombre del Empleado', 'required': 'required','onkeyup':'replaceCaratect(this)'}),
            'apellido_emp' : forms.TextInput(attrs={'class':'form-control', 'name': 'apellida_emp', 'placeholder': 'Apellido del Empleado', 'required': 'required','onkeyup':'replaceCaratect(this)'}),
            'ci_empe' : forms.TextInput(attrs={'class':'form-control', 'name':'apellido_emp', 'placeholder': 'Nro. Cédula', 'required':'required','onkeyup':'replaceABC(this)'}),
			'disponible' : forms.CheckboxInput(attrs={'class':'form-control', 'type': 'checkbox','name': 'disponible'}),
            'id_servicio' : forms.Select(attrs={'class':'form-control', 'id': 'id_servicio','required':'required' ,'name':'id_servicio'}),        
		}