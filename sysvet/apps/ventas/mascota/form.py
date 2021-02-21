from django import forms

from .models import Mascota, Especie

class MascotaForm(forms.ModelForm):
    """[summary]

    Args:
        forms ([MascotaForm]): [Formulario de la mascota]
    """    
    class Meta:
        model = Mascota
        fields = '__all__'   
        widgets = {
            'sexo' : forms.Select(attrs={'class':'form-control', 'id': 'sexo','required':'required' ,'name':'sexo'}),
            'id_raza' : forms.Select(attrs={'class':'form-control', 'id': 'id_raza','required':'required' ,'name':'id_raza'}),
            'id_cliente' : forms.Select(attrs={'class':'form-control', 'id': 'id_cliente','required':'required' ,'name':'id_cliente'})
		}

class EspecieForm(forms.ModelForm):
    """[summary]

    Args:
        forms ([EspecieForm]): [Formulario de Especie]
    """    
    class Meta:
        model = Especie
        fields = '__all__'       
        widgets = {
            'nombre_especie' : forms.TextInput(attrs={'class':'form-control','data-validate-length-range':'20', 
                'data-validate-words':'1', 'name': 'nombre_especie', 'placeholder': 'Nombre de la Especie', 'required': 'required'}),
		}