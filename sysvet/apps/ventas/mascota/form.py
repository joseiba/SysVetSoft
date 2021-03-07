from django import forms

from .models import Mascota, Especie, Raza

class MascotaForm(forms.ModelForm):
    """[summary]

    Args:
        forms ([MascotaForm]): [Formulario de la mascota]
    """    
    class Meta:
        model = Mascota
        fields = '__all__'   
        widgets = {
            'nombre_mascota': forms.TextInput(attrs={'class':'form-control','data-validate-length-range':'20', 
                'data-validate-words':'1', 'name': 'nombre_mascota', 'placeholder': 'Nombre de la mascota', 'required': 'required'}),
            'tatuaje': forms.TextInput(attrs={'class':'form-control optional', 'name': 'tatuaje', 'placeholder': 'Tatuaje'}),
            'edad': forms.TextInput(attrs={'class':'form-control optional', 'name': 'edad', 'placeholder': 'Edad'}),
            'sexo' : forms.Select(attrs={'class':'form-control', 'id': 'sexo','required':'required' ,'name':'sexo'}),
            'fecha_nacimiento' : forms.TextInput(attrs={'class':'form-control optional date', 'type': 'date','name':'fecha_nacimiento'}),
            'peso': forms.TextInput(attrs={'class':'form-control','data-validate-length-range':'20', 
                'data-validate-words':'1', 'name': 'peso', 'placeholder': 'Peso', 'required': 'required'}),
            'imagen': forms.FileInput(attrs={'type': 'file', 'name':'imagen', 'id': 'imageInput', 'accept':'image/*'}),
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


class RazaForm(forms.ModelForm):
    """[summary]

    Args:
        forms ([RazaForm]): [Formulario de Raza]
    """    
    class Meta:
        model = Raza
        fields = '__all__'       
        widgets = {
            'nombre_raza' : forms.TextInput(attrs={'class':'form-control','data-validate-length-range':'20', 
                'data-validate-words':'1', 'name': 'nombre_raza', 'placeholder': 'Nombre de la Raza', 'required': 'required'}),
            'id_especie' : forms.Select(attrs={'class':'form-control', 'id': 'id_especie','required':'required' ,'name':'id_especie'}),
		}        