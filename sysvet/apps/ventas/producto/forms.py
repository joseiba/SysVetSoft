from django import forms

from apps.ventas.producto.models import TipoProducto, Deposito, Producto

class TipoProductoForm(forms.ModelForm):
    """[summary]

    Args:
        forms ([TipoProductoForm]): [Formulario de tipo de producto]
    """    
    class Meta:
        model = TipoProducto
        exclude = ['is_active']
        widgets = {
            'codigo_tipo' : forms.TextInput(attrs={'class':'form-control', 'name': 'codigo_tipo', 'placeholder': 'Codigo Tipo', 'required': 'required', 'onkeyup':'replaceDirection(this)'}),
            'nombre_tipo' : forms.TextInput(attrs={'class':'form-control', 'name': 'nombre_tipo', 'placeholder': 'Nombre Tipo Producto', 'required': 'required', 'onkeyup':'replaceCaratect(this)'}),
            'vence' : forms.Select(attrs={'class':'form-control', 'id': 'vence','required':'required' ,'name':'vence'}),
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
			'descripcion' : forms.TextInput(attrs={'class':'form-control', 'name': 'descripcion', 'placeholder': 'Descripcion', 'required': 'required', 'onkeyup':'replaceCaratect(this)'}),
			
		}


class ProductoForm(forms.ModelForm):
    """[summary]

    Args:
        forms ([ProductoForm]): [Formulario de producto]
    """    
    class Meta:
        model = Producto
        exclude = ['is_active']
        widgets = {
			'codigo_producto' : forms.TextInput(attrs={'class':'form-control', 'name': 'codigo_producto','autocomplete': 'off' ,'placeholder': 'Codigo Producto', 'required': 'required', 'onkeyup':'replaceDirection(this)'}),
            'nombre_producto': forms.TextInput(attrs={'class':'form-control', 'name': 'nombre_producto', 'autocomplete': 'off' ,'placeholder': 'Nombre del producto', 'required': 'required', 'onkeyup':'replaceCaratect(this)'}),
            'descripcion' : forms.TextInput(attrs={'class':'form-control', 'name': 'descripcion', 'autocomplete': 'off' ,'placeholder': 'Descripcion', 'required': 'required', 'onkeyup':'replaceDirection(this)'}),
            'fecha_vencimiento' : forms.TextInput(attrs={'class':'form-control','type':'text', 'autocomplete': 'off' ,'id':'datepicker' ,'name': 'fecha_vencimiento', 
                'placeholder': 'Fecha de Vencimiento'}),
            'fecha_baja' : forms.TextInput(attrs={'class':'form-control','type':'text', 'autocomplete': 'off' ,'name': 'fecha_baja', 
                'placeholder': 'Fecha de Baja'}),
            'fecha_movimiento' : forms.TextInput(attrs={'class':'form-control','type':'text', 'autocomplete': 'off' ,
                'name': 'fecha_movimiento', 'placeholder': 'Fecha de Movimiento'}),
            'fecha_compra' : forms.TextInput(attrs={'class':'form-control','type':'text', 'name': 'fecha_compra', 'autocomplete': 'off' ,
                'placeholder': 'Fecha de Compra', 'readonly': 'readonly'}),
			'precio_compra': forms.TextInput(attrs={'class':'form-control', 'name': 'precio_compra', 'autocomplete': 'off' ,'placeholder': 'Precio de compra', 'onkeyup':'replaceDirection(this)'}),
            'precio_venta': forms.TextInput(attrs={'class':'form-control', 'name': 'precio_venta','autocomplete': 'off' , 'placeholder': 'Precio de Venta', 'onkeyup':'replaceDirection(this)'}),
            'stock_minimo': forms.TextInput(attrs={'class':'form-control', 'name': 'stock_minimo','autocomplete': 'off' , 'placeholder': 'Stock Minimo', 'onkeyup':'replaceDirection(this)'}),
            'lote': forms.TextInput(attrs={'class':'form-control', 'name': 'lote', 'placeholder': 'Lote', 'autocomplete': 'off' ,'onkeyup':'replaceDirection(this)'}),
            'stock': forms.TextInput(attrs={'id':'stock', 'class':'form-control', 'name': 'stock', 'autocomplete': 'off' ,'placeholder': 'Stock', 'onkeyup':'replaceDirection(this)'}),
            'tipo_producto' : forms.Select(attrs={'class':'form-control', 'id': 'tipo_producto', 'autocomplete': 'off' ,'required':'required' ,'name':'tipo_producto'}),
            'id_deposito' : forms.Select(attrs={'class':'form-control', 'id': 'id_deposito','autocomplete': 'off' ,'required':'required' ,'name':'id_deposito'})
		}