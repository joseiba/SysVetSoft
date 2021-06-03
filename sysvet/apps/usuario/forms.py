from django.contrib.auth.forms import AuthenticationForm,  UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group, Permission
from django.forms import *


from apps.usuario.models import User

class FormLogin(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(FormLogin, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'input100'
        self.fields['username'].widget.attrs['placeholder'] = 'Nombre de usuario'
        self.fields['password'].widget.attrs['class'] = 'input100'
        self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'


class UserForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

    class Meta():
        model = User
        fiels = ("first_name", "last_name", "email", "username", "groups", "password1", "password2")
        widgets = {
            'first_name': TextInput(
                attrs={
                    'class': 'form-control','name': 'first_name', 'placeholder': 'Ingrese el nombre del usuario','onkeyup':'replaceDirection(this)', 'required': 'required', 'autocomplete':"off"
                }
            ),
            'last_name': TextInput(
                attrs={
                    'class': 'form-control','name': 'last_name', 'placeholder': 'Ingrese el apellido del usuario','onkeyup':'replaceDirection(this)', 'required': 'required', 'autocomplete':"off"
                }
            ),
            'email': TextInput(
                attrs={
                    'class':'form-control optional', 'placeholder': 'Email','name':'email', 'type':'email', 'id':'email', 'autocomplete':"off"
                }
            ),
            'username': TextInput(
                attrs={
                    'class': 'form-control','name': 'username', 'placeholder': 'Nombre de usuario','onkeyup':'replaceDirection(this)', 'required': 'required', 'autocomplete':"off"
                }
            ),
            'groups' : Select(attrs={'class':'form-control', 'id': 'group_select' ,'name':'groups', 'required': 'required'})
        }
        exclude = ['user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_active', 'is_staff', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        for grupo in self.cleaned_data['groups']:
            user.groups.add(grupo)
        return user


class UserFormChange(UserChangeForm):

    password1 = CharField(required=False,label="Contraseña",
                                widget=PasswordInput(attrs={
                                    'class':'form-control',
                                },))
    password2 = CharField(required=False,label="Confirmar Contraseña",
                                widget=PasswordInput(attrs={
                                        'class': 'form-control',
                                    }
                                ),
                                help_text="Ingrese la misma contraseña que la anterior, para verificación.")
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username","profile","groups")
        widgets = {
            'first_name': TextInput(
                attrs={
                    'class': 'form-control','name': 'first_name', 'placeholder': 'Ingrese el nombre del usuario','onkeyup':'replaceDirection(this)', 'required': 'required', 'autocomplete':"off"
                }
            ),
            'last_name': TextInput(
                attrs={
                    'class': 'form-control','name': 'last_name', 'placeholder': 'Ingrese el apellido del usuario','onkeyup':'replaceDirection(this)', 'required': 'required', 'autocomplete':"off"
                }
            ),
            'email': TextInput(
                attrs={
                    'class':'form-control optional', 'placeholder': 'Email','name':'email', 'type':'email', 'id':'email', 'autocomplete':"off"
                }
            ),
            'username': TextInput(
                attrs={
                    'class': 'form-control','name': 'username', 'placeholder': 'Nombre de usuario','onkeyup':'replaceDirection(this)', 'required': 'required', 'autocomplete':"off"
                }
            ),
            'groups' : Select(attrs={'class':'form-control', 'id': 'group_select' ,'name':'groups'})
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("La contraseñas no coinciden")
        return password2

    def save(self, commit=True):
        form = super()
        if form.is_valid():
            user = form.save(commit=False)
            if self.cleaned_data['password1'] != '':
                user.set_password(self.cleaned_data["password1"])
            if commit:
                user.save()
            user.groups.clear()
            for grupo in self.cleaned_data['groups']:
                user.groups.add(grupo)
            return user


queryset = ["user",
"deposito",
"producto",
"tipoproducto",
"productostock",
"ciudad",
"cliente",
"especie",
"fichamedica",
"historicofichamedica",
"vacuna",
"raza",
"mascota",
"consulta",
"antiparasitario",
"reserva",
"confiempresa",
"servicio",
"empleado",
"facturacompra",
"pago",
"proveedor",
"pedido",
"facturadet",
"pedidocabecera",
"pedidodetalle",
"facturacabeceraventa",
"pagoventa",
"productoservicios",
"facturadetalleventa"]

class GroupForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['permissions'].queryset = Permission.objects.filter(content_type__model__in=queryset)

    class Meta:
        model = Group
        fields = ('name', 'permissions')
        widgets = {
            'name': TextInput(attrs={
                'class':'form-control'
            }),
            'permissions': CheckboxSelectMultiple(),
        }


class GroupChangeForm(ModelForm):

    class Meta:
        model = Group
        fields = ('name', 'permissions')
        widgets = {
            'name': TextInput(attrs={
                'class':'form-control'
            }),
            'permissions': CheckboxSelectMultiple(),
        }