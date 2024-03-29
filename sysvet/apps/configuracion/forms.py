from django import forms

from apps.configuracion.models import Servicio, Empleado, ConfiEmpresa, TipoVacuna

class ConfiEmpresaForm(forms.ModelForm):
    class Meta:
        model = ConfiEmpresa
        exclude = ['id_confi']
        widgets = {
            'nombre_empresa' : forms.TextInput(attrs={'class':'form-control', 'autocomplete': 'off','name': 'nombre_empresa', 'placeholder': 'Nombre de la empresa', 'required': 'required','onkeyup':'replaceDirection(this)'}),
            'direccion' : forms.TextInput(attrs={'class':'form-control', 'autocomplete': 'off','name': 'direccion', 'placeholder': 'Direccion de la empresa', 'required': 'required','onkeyup':'replaceDirection(this)'}),
            'cuidad' : forms.TextInput(attrs={'class':'form-control', 'autocomplete': 'off','name': 'cuidad', 'placeholder': 'Cuidad de la empresa', 'required': 'required','onkeyup':'replaceDirection(this)'}),
            'telefono' : forms.TextInput(attrs={'class':'form-control', 'autocomplete': 'off','name': 'telefono', 'placeholder': 'Telefono de la empresa', 'required': 'required','onkeyup':'replaceABC(this)'}),
            'fecha_inicio_timbrado': forms.TextInput(attrs={'class': 'form-control',
                                            'id': 'datePick-emision',
                                            'placeholder': 'Selecciona la fecha de inicio',
                                            'name':'fecha_inicio_timbrado',
                                            'autocomplete': 'off',
                                            'required': 'required'}),
            'fecha_fin_timbrado': forms.TextInput(attrs={'class': 'form-control',
                                            'id': 'datePick-vencimiento',
                                            'placeholder': 'Selecciona la fecha de vencimiento',
                                            'name':'fecha_fin_timbrado',
                                            'autocomplete': 'off',
                                            'required': 'required'}),
            'nro_timbrado': forms.TextInput(attrs={'class': 'form-control', 'name': 'nro_timbrado','id':'nro_timbrado','autocomplete': 'off','placeholder': 'Escriba el nro del timbrado','required':'required','onkeyup':'replaceABC(this)'}),
            'ruc_empresa': forms.TextInput(attrs={'class': 'form-control', 'name': 'ruc_empresa','autocomplete': 'off','placeholder': 'Escriba el RUC','required':'required','onkeyup':'replaceABC(this)'}),
            'apertura_caja_inicial' : forms.TextInput(attrs={'class':'form-control', 'autocomplete': 'off','name': 'apertura_caja_inicial', 'placeholder': 'Ingrese el monto inicial de la caja', 'required': 'required','onkeyup':'replaceABC(this)'}),
			'ubicacion_deposito_inicial' : forms.TextInput(attrs={'class':'form-control', 'autocomplete': 'off','name': 'ubicacion_deposito_inicial', 'placeholder': 'Deposito inicial', 'required': 'required','onkeyup':'replaceDiretion(this)'}),
            'dias_a_vencer' : forms.TextInput(attrs={'class':'form-control', 'autocomplete': 'off','name': 'dias_a_vencer', 'placeholder': 'Dias Productos a Vencer', 'required': 'required','onkeyup':'replaceABC(this)'}),
            'dias_alert_vacunas' : forms.TextInput(attrs={'class':'form-control', 'autocomplete': 'off','name': 'dias_alert_vacunas', 'placeholder': 'Dias aviso proximas vacunaciones', 'required': 'required','onkeyup':'replaceABC(this)'}),

		}

class ServicioForm(forms.ModelForm):
    """[summary]

    Args:
        forms ([ServicioForm]): [Formulario de servicios]
    """    
    class Meta:
        model = Servicio
        exclude = ['is_active']
        widgets = {
            'cod_serv' : forms.TextInput(attrs={'class':'form-control', 'name': 'cod_serv', 'placeholder': 'Nombre del Servicio', 
                'autocomplete': 'off','required': 'required','onkeyup':'replaceCaratect(this)'}),
			'nombre_servicio' : forms.TextInput(attrs={'class':'form-control','autocomplete': 'off', 'name': 'nombre_servicio',
                'placeholder': 'Nombre del Servicio', 'required': 'required','onkeyup':'replaceCaratect(this)'}),
			'precio_servicio' : forms.TextInput(attrs={'class':'form-control', 'name': 'precio_servicio', 
                'placeholder': 'Precio del Servicio', 'autocomplete': 'off','required': 'required','onkeyup':'replaceABC(this)'}),
            'min_serv' : forms.TextInput(attrs={'class':'form-control', 'name': 'min_serv', 
                'placeholder': 'Tiempo del servicio en minutos', 'autocomplete': 'off','required': 'required','onkeyup':'replaceABC(this)'})
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
            'nombre_emp' : forms.TextInput(attrs={'class':'form-control', 'name': 'nombre_emp', 
                'placeholder': 'Nombre del Empleado', 'required': 'required','onkeyup':'replaceCaratect(this)', 'autocomplete': 'off'}),
            'apellido_emp' : forms.TextInput(attrs={'class':'form-control', 'name': 'apellida_emp', 
                'placeholder': 'Apellido del Empleado', 'required': 'required','onkeyup':'replaceCaratect(this)', 'autocomplete': 'off'}),
            'ci_empe' : forms.TextInput(attrs={'class':'form-control', 'name':'apellido_emp', 
                'placeholder': 'Nro. Cédula', 'required':'required','onkeyup':'replaceABC(this)', 'autocomplete': 'off'}),
			'disponible' : forms.CheckboxInput(attrs={'class':'form-control', 'type': 'checkbox','name': 'disponible'}),
            'id_servicio' : forms.Select(attrs={'class':'form-control', 'id': 'id_servicio','required':'required' ,'name':'id_servicio'}),        
		}


class TipoVacunaForm(forms.ModelForm):
    """[summary]

    Args:
        forms ([TipoVacunaForm]): [Formulario de vacunas]
    """    
    class Meta:
        model = TipoVacuna
        fields = '__all__'        
        widgets = {
            'id_producto' : forms.Select(attrs={'class':'form-control', 'id': 'id_producto' ,'name':'id_producto', 'readonly': 'readonly', 
                'onfocus': 'this.size=5;', 'onblur': 'this.size=1;', 'onchange': 'this.size=1; this.blur();'}),
            'nombre_vacuna' : forms.TextInput(attrs={'class':'form-control', 'name': 'nombre_vacuna', 'placeholder': 'Vacuna Dosis', 'required': 'required','autocomplete': 'off','onkeyup':'replaceCaratect(this)'}),
            'periodo_aplicacion' : forms.TextInput(attrs={'class':'form-control', 'name': 'periodo_aplicacion', 'placeholder': 'Periodo de Aplicacion', 
                'required': 'required','autocomplete': 'off'  ,'onkeyup':'replaceABC(this)'}),
            'multi_aplicaciones' : forms.Select(attrs={'class':'form-control', 'id': 'multi_aplicaciones','required':'required' ,'name':'multi_aplicaciones'}),
		}



