from django import forms

from .models import Mascota

class MascotaForm(forms.ModelForm):
    """[summary]

    Args:
        forms ([MascotaForm]): [Formulario de la mascota]
    """    
    class Meta:
        model = Mascota
        fields = '__all__'   
        widgets = {
            'sexo' : forms.Select(attrs={'class':'form-control', 'id': 'sexo','required':'required' ,'name':'sexo'})
		}