from django import forms

from .models import Reserva

class ReservaForm(forms.ModelForm):
    """[summary]

    Args:
        forms ([ReservaForm]): [Formulario de reservas]
    """   
    class Meta:
        model = Reserva
        exclude = ['is_active']
        widgets = {
			'descripcion' : forms.TextInput(attrs={'class':'form-control', 'name': 'descripcion', 'placeholder': 'Descripción de la reserva','onkeyup':'replaceDirection(this)'}),
            'fecha_reserva' : forms.TextInput(attrs={'class':'form-control', 'type': 'date','name':'fecha_reserva', 'required': 'required'}),
            'hora_reserva' : forms.TextInput(attrs={'class':'form-control', 'type': 'time','name':'hora_reserva', 'required': 'required'}),
            'id_servicio' : forms.Select(attrs={'class':'form-control', 'id': 'id_servicio','required':'required' ,'name':'id_servicio'}),        
            'id_cliente' : forms.Select(attrs={'class':'form-control', 'id': 'id_cliente','required':'required' ,'name':'id_cliente'})
		}
