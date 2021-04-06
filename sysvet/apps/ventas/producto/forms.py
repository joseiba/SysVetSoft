from django import forms

from .models import TipoProducto, Deposito, Producto

class TipoProductoForm(forms.ModelForm):
    """[summary]

    Args:
        forms ([TipoProductoForm]): [Formulario de tipo de producto]
    """    
    class Meta:
        model = TipoProducto
        fields = '__all__'
        widgets = {
			'nombre_tipo' : forms.TextInput(attrs={'class':'form-control', 'name': 'nombre_tipo', 'placeholder': 'Nombre Tipo Producto', 'required': 'required'}),
			'fecha_alta' : forms.TextInput(attrs={'class':'form-control','type':'datetime',
                'name': 'fecha_alta', 'placeholder': 'Fecha de Alta', 'readonly': 'readonly'}),
			'fecha_baja' : forms.TextInput(attrs={'class':'form-control','type':'datetime', 'name': 'fecha_baja', 
                'placeholder': 'Fecha de Baja', 'readonly': 'readonly'}),
			
		}


class DepositoForm(forms.ModelForm):
    """[summary]

    Args:
        forms ([DepositoForm]): [Formulario de deposito]
    """    
    class Meta:
        model = Deposito
        fields = '__all__'
        widgets = {
			'descripcion' : forms.TextInput(attrs={'class':'form-control', 'name': 'descripcion', 'placeholder': 'Descripcion', 'required': 'required'}),
			
		}


class ProductoForm(forms.ModelForm):
    """[summary]

    Args:
        forms ([ProductoForm]): [Formulario de producto]
    """    
    class Meta:
        model = Producto
        fields = '__all__'
        widgets = {
			'nombre_producto': forms.TextInput(attrs={'class':'form-control','data-validate-length-range':'20', 
                'data-validate-words':'1', 'name': 'nombre_producto', 'placeholder': 'Nombre del producto', 'required': 'required'}),
            'descripcion' : forms.TextInput(attrs={'class':'form-control', 'name': 'descripcion', 'placeholder': 'Descripcion', 'required': 'required'}),
            'fecha_vencimiento' : forms.TextInput(attrs={'class':'form-control date', 'type': 'date','name':'fecha_vencimiento'}),
            'fecha_baja' : forms.TextInput(attrs={'class':'form-control date', 'type': 'date','name':'fecha_baja'}),
            'fecha_movimiento' : forms.TextInput(attrs={'class':'form-control date', 'type': 'date','name':'fecha_movimiento'}),
            'fecha_compra' : forms.TextInput(attrs={'class':'form-control date', 'type': 'date','name':'fecha_compra'}),
			'precio_compra': forms.TextInput(attrs={'class':'form-control', 'name': 'precio_compra', 'placeholder': 'Precio de compra'}),
            'precio_venta': forms.TextInput(attrs={'class':'form-control', 'name': 'precio_venta', 'placeholder': 'Precio de Venta'}),
            'stock_minimo': forms.TextInput(attrs={'class':'form-control', 'name': 'stock_minimo', 'placeholder': 'Stock Minimo'}),
            'stock': forms.TextInput(attrs={'class':'form-control', 'name': 'stock_minimo', 'placeholder': 'Stock'}),
            'tipo_producto' : forms.Select(attrs={'class':'form-control', 'id': 'tipo_producto','required':'required' ,'name':'tipo_producto'}),
            'id_deposito' : forms.Select(attrs={'class':'form-control', 'id': 'id_deposito','required':'required' ,'name':'id_deposito'})
		}