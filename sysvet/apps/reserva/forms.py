from django import forms

from .models import Servicio, Reserva


class ServicioForm(forms.ModelForm):
    """[summary]

    Args:
        forms ([ServicioForm]): [Formulario de servicios]
    """    
    class Meta:
        model = Servicio
        exclude = ['is_active']
        widgets = {
			'nombre_servicio' : forms.TextInput(attrs={'class':'form-control','data-validate-length-range':'20', 
                'data-validate-words':'4', 'name': 'nombre_servicio', 'placeholder': 'Nombre del Servicio', 'required': 'required','onkeyup':'replaceCaratect(this)'}),
			'precio_servicio' : forms.TextInput(attrs={'class':'form-control', 'name': 'precio_servicio', 'placeholder': 'Precio del Servicio', 
                'required': 'required','onkeyup':'replaceABC(this)'}),
		}

class ReservaForm(forms.ModelForm):
    """[summary]

    Args:
        forms ([ReservaForm]): [Formulario de reservas]
    """   
    class Meta:
        model = Reserva
        exclude = ['is_active']
        widgets = {
			'descripcion' : forms.TextInput(attrs={'class':'form-control', 'name': 'descripcion', 'placeholder': 'Descripción de la reserva', 'required': 'required','onkeyup':'replaceCaratect(this)'}),
            'fecha_reserva' : forms.TextInput(attrs={'class':'form-control', 'type': 'date','name':'fecha_reserva', 'required': 'required'}),
            'hora_reserva' : forms.TextInput(attrs={'class':'form-control', 'type': 'time','name':'hora_reserva', 'required': 'required'}),
            'id_servicio' : forms.Select(attrs={'class':'form-control', 'id': 'id_servicio','required':'required' ,'name':'id_servicio'}),        
            'id_mascota' : forms.Select(attrs={'class':'form-control', 'id': 'id_mascota','required':'required' ,'name':'id_mascota'}),
            'id_cliente' : forms.Select(attrs={'class':'form-control', 'id': 'id_cliente','required':'required' ,'name':'id_cliente'})
		}
