from django import forms

from .models import Cliente

class ClienteForm(forms.ModelForm):
    """[summary]

    Args:
        forms ([ClienteForm]): [Formulario de cliente]
    """    
    class Meta:
        model = Cliente
        fields = '__all__'        