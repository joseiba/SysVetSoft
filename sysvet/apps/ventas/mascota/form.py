from django import forms

from .models import Mascota, Especie, Raza, FichaMedica, Vacuna, Consulta, Antiparasitario

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
                'data-validate-words':'1', 'name': 'nombre_mascota','onkeyup':'replaceCaratect(this)','placeholder': 'Nombre de la mascota', 'required': 'required'}),
            'tatuaje': forms.TextInput(attrs={'class':'form-control optional', 'onkeyup':'replaceCaratect(this)','name': 'tatuaje', 'placeholder': 'Tatuaje'}),
            'edad': forms.TextInput(attrs={'class':'form-control optional', 'name': 'edad', 'placeholder': 'Edad','onkeyup':'replaceDirection(this)'}),
            'sexo' : forms.Select(attrs={'class':'form-control', 'id': 'sexo','required':'required' ,'name':'sexo'}),
            'fecha_nacimiento' : forms.TextInput(attrs={'class':'form-control optional date', 'type': 'date','name':'fecha_nacimiento'}),
            'peso': forms.TextInput(attrs={'class':'form-control','onkeyup':'replaceDirection(this)', 'name': 'peso', 'placeholder': 'Peso', 'required': 'required'}),
            'color_pelaje' : forms.TextInput(attrs={'class':'form-control', 'type': 'color','name':'color_pelaje','placeholder': 'Color Pelaje'}),
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
            'nombre_especie' : forms.TextInput(attrs={'class':'form-control','onkeyup':'replaceCaratect(this)' ,'id': 'nombre_especie','data-validate-length-range':'20', 
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
            'nombre_raza' : forms.TextInput(attrs={'class':'form-control', 'id': 'nombre_raza','data-validate-length-range':'20', 
                'data-validate-words':'1', 'name': 'nombre_raza','onkeyup':'replaceCaratect(this)','placeholder': 'Nombre de la Raza', 'required': 'required'}),
            'id_especie' : forms.Select(attrs={'class':'form-control', 'id': 'id_especie','required':'required' ,'name':'id_especie'}),
		}        


#Forms para las fichas medicas
class FichaMedicaForm(forms.ModelForm):
    """[summary]

    Args:
        forms ([FichaMedicaForm]): [Formulario de Ficha de Medica]
    """ 
    class Meta:
        model = FichaMedica
        exclude = ['fecha_create']
        widgets = {
        'id_mascota' : forms.HiddenInput(),
        }

class VacunaForm(forms.ModelForm):
    """[summary]

    Args:
        forms ([VacunaForm]): [Formulario de Vacuna]
    """ 
    class Meta:
        model = Vacuna
        fields = '__all__'   
        widgets = {
        'proxima_vacuna' : forms.Select(attrs={'class':'form-control', 'id': 'id_vacuna','name':'proxima_vacuna'}),
        'id_vacuna' : forms.Select(attrs={'class':'form-control', 'id': 'id_vacuna','name':'id_vacuna'}),
        'fecha_aplicacion': forms.TextInput(attrs={'class': 'form-control',
                                            'id': 'datePick-aplicacion',
                                            'placeholder': 'Fecha Aplicacion',
                                            'name':'fecha_aplicacion',
                                            'autocomplete': 'off',
                                            'readonly': "readonly",
                                            'disabled': 'disabled'}),
        'fecha_proxima_aplicacion': forms.TextInput(attrs={'class': 'form-control',
                                            'id': 'datePick-proxima-aplicacion',
                                            'placeholder': 'Proxima Aplicacion',
                                            'name':'fecha_proxima_aplicacion',
                                            'readonly': "readonly",
                                            'autocomplete': 'off'}),
        'id_ficha_medica' : forms.HiddenInput(),        
        }

class ConsultaForm(forms.ModelForm):
    """[summary]

    Args:
        forms ([ConsultaForm]): [Formulario de Consulta]
    """ 
    class Meta:
        model = Consulta
        fields = '__all__'   
        widgets = {
        'diagnostico': forms.Textarea(attrs={'class':'form-control optional','name': 'diagnostico', 'rows': '2','placeholder': 'Diagnostico','onkeyup':'replaceDirection(this)'}),
        'tratamiento': forms.Textarea(attrs={'class':'form-control optional', 'rows': '2', 'name': 'tratamiento', 'placeholder': 'Tratamiento','onkeyup':'replaceDirection(this)'}),
        'medicamento': forms.Textarea(attrs={'class':'form-control optional', 'rows': '2', 'name': 'medicamento', 'placeholder': 'Medicamento','onkeyup':'replaceDirection(this)'}),
        'proximo_tratamiento' : forms.Textarea(attrs={'class':'form-control optional', 'rows': '2', 'type': 'text','name':'proximo_tratamiento','onkeyup':'replaceDirection(this)'}),
        'id_ficha_medica' : forms.HiddenInput(),
        }

class AntiparasitarioForm(forms.ModelForm):
    """[summary]

    Args:
        forms ([AntiparasitarioForm]): [Formulario de Antiparasitario]
    """ 
    class Meta:
        model = Antiparasitario
        fields = '__all__'   
        widgets = {
        'antiparasitario': forms.TextInput(attrs={'class':'form-control optional', 'name': 'antiparasitario', 'placeholder': 'Antiparasitario','onkeyup':'replaceDirection(this)'}),
        'proximo_antiparasitario' : forms.TextInput(attrs={'class':'form-control optional', 'type': 'text','name':'proximo_antiparasitario','onkeyup':'replaceDirection(this)'}),  
        'id_ficha_medica' : forms.HiddenInput(),
        }

