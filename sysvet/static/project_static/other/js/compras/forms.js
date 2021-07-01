var tblFactura;

// Estructura para el detalle de facturas
var factura = {
    items: {
        proveedor: '',
        nro_factura: '',
        nro_timbrado: '',
        fecha_vencimiento: '',
        fecha_emision: '',
        total_iva: 0,
        total_factura: 0,
        products: []
    },
    calc_invoice: function () {
        var subtotal = 0
        $.each(this.items.products, function (pos, dict) {
            var dic_precio_format ;
            if(precio_compra_action != 'S'){
                dic_precio_format = dict.precio_compra.split('.')
            }
            else{
                dic_precio_format = dict.precio_compra_viejo.split('.')
            }
            var dic_sum = "";

            for (let index = 0; index < dic_precio_format.length; index++) {
                dic_sum += dic_precio_format[index];                
            }
            dict.subtotal = dict.cantidad * parseFloat(dic_sum);
            subtotal += dict.subtotal;
        })
        var value_formated = add_miles(subtotal)
        this.items.total_factura = Math.round(subtotal);
        this.items.total_iva = Math.round(subtotal/11);
        $('#totalIva').val(this.items.total_iva); // el iva en el template
        $('#total').val(value_formated); // para el total
    },
    add: function (item) {
        this.items.products.push(item);
        this.list();
    },
    list: function () {
        this.calc_invoice()
        tblFactura = $('#tblFactura').DataTable({
            responsive: true,
            searching: false,
            destroy: true,
            data: this.items.products,
            ordering: false,
            columns: [
                {"data": "codigo_producto"},
                {"data": "nombre"},
                {"data": "description"},
                {"data": "precio_compra"},
                {"data": "cantidad"},
                {"data": "subtotal"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: "text-center",
                    width: "5%",
                    orderable: false,
                },
                
                {
                    targets: [1],
                    class: "",
                    width: "10%",
                    orderable: false,                
                },
                {
                    targets: [2],
                    class: "",
                    width: "30%",
                    orderable: false,                
                },
                {
                    targets: [3],
                    class: "text-center my-0 ",
                    orderable: false,
                    render: function (data, type, row) {
                        if(precio_compra_action != 'S'){
                            return '<input type="text" name="precio_compra" id="precio_compra" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.precio_compra + '">';
                        }
                        return "Gs. " + row.precio_compra_viejo;
                    }
                },
                {
                    targets: [4],
                    width: "10%",
                    class: "text-center",
                    orderable: false,  
                    /*render: function (data, type, row) {
                        if(action == "A"){
                            if(row.cantidad_pedido === "-"){
                                return '<input type="text" name="cantidad" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.cantidad + '">';
                            }else{
                                return '<input type="text" name="cantidad" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.cantidad + '">';
                            }    
                        }else{  
                            return '<input type="text" name="cantidad" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.cantidad + '">';
                        }                                            
                    }   */              
                },
                {
                    targets: [5],
                    class: "text-center my-0 ",
                    orderable: false,
                    render: function (data, type, row) {
                        var amount_formated = add_miles(data)
                        return 'Gs. ' + amount_formated
                    }
                },
                /*{
                    targets: [5],
                    class: "text-center",
                    width: "5%",
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger m-0 p-0"><i class="fa fa-trash m-1" style="color: white" aria-hidden="true"></i>\n</i></a>'
                    }
                },*/
            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {
                $(row).find('input[name="cantidad"]').TouchSpin({
                    min: 0,
                    max: 1000000000,
                    step: 1,
                    boostat: 5,
                    maxboostedstep: 10,
                }).keypress(function (e) {
                    return validate_form_text('numbers', e, null);
                });
            },
            language: {                    
                decimal: "",
                emptyTable: "No hay información",
                info: "Mostrando _START_ a _END_ de _TOTAL_ Entradas",
                infoEmpty: "Mostrando 0 de 0 Entradas",
                infoFiltered: "(Filtrado de _MAX_ total entradas)",
                infoPostFix: "",
                thousands: ",",
                lengthMenu: "Mostrar _MENU_ Entradas",
                loadingRecords: "Cargando...",
                processing: "Procesando...",
                search: "Buscar:",
                zeroRecords: "Sin resultados encontrados",
                paginate: {
                    first: "Primero",
                    last: "Ultimo",
                    next: "Siguiente",
                    previous: "Anterior",
                },
            },
        });
    }
}

$(function () {
    $('#search').on('select2:select', function (e) {
        var data = e.params.data;
        if(data.cantidad_pedido === "-"){
                data['cantidad'] = 1;
        }else{
                data['cantidad'] = parseInt(data.cantidad_pedido);
            }
        
        //data['subtotal'] = 0;
        //se agrega los datos a la estructura
        factura.add(data)
        // borra luego de la seleccion
        $(this).val('').trigger('change.select2');
    });

    $('.btnRemoveAll').on('click', function () {
        if (factura.items.products.length === 0) return false;
        alert_delete('Notificación', '¿Estás seguro de eliminar todos los detalles de la factura', function () {
            factura.items.products = [];
            factura.list();
        });
    });

    $('#tblFactura').on('click', 'a[rel="remove"]', function () {
        var tr = tblFactura.cell($(this).closest('td, li')).index();
        factura.items.products.splice(tr.row, 1);
        factura.list();
    }).on('change', 'input[name="cantidad"]', function () {
        var cant = parseInt($(this).val());
        var tr = tblFactura.cell($(this).closest('td, li')).index();
        factura.items.products[tr.row].cantidad = cant;
        factura.calc_invoice();
        // el 5 es el lugar donde tiene que estar el subtotal
        $('td:eq(5)', tblFactura.row(tr.row).node()).html('Gs.' +  add_miles(factura.items.products[tr.row].subtotal));
    }).on('change', 'input[name="descripcion"]', function (){
        var descripcion = $(this).val();
        var tr = tblFactura.cell($(this).closest('td, li')).index();
        factura.items.products[tr.row].description = descripcion;
    }).on('keyup', 'input[name="precio_compra"]', function(event) {
        $(event.target).val(function (index, value ) {
            var cant = add_miles($(this).val());
            var tr = tblFactura.cell($(this).closest('td, li')).index();
            factura.items.products[tr.row].precio_compra = cant;
            factura.calc_invoice();
            // el 5 es el lugar donde tiene que estar el subtotal
            $('td:eq(5)', tblFactura.row(tr.row).node()).html('Gs.' +  add_miles(factura.items.products[tr.row].subtotal));
            return value.replace(/\D/g, "")
                        .replace(/([0-9])([0-9]{3})$/, '$1.$2')
                        .replace(/\B(?=(\d{3})+(?!\d)\.?)/g, ".");
        });
    })

    $('form').on('submit', function (e) {
        e.preventDefault();
        factura.items.proveedor = $('select[name="id_proveedor"]').val();
        factura.items.fecha_emision = $('input[name="fecha_emision"]').val();
        factura.items.fecha_vencimiento = $('input[name="fecha_vencimiento"]').val();
        factura.items.nro_factura = $('input[name="nro_factura"]').val();
        factura.items.nro_timbrado = $('input[name="nro_timbrado"]').val();
        var parameters = new FormData();
        parameters.append('factura', JSON.stringify(factura.items));
        var csrf = $('input[name="csrfmiddlewaretoken"]').val();
        parameters.append('csrfmiddlewaretoken', csrf);
        submit_with_ajax(window.location.pathname, 'Noticicación', '¿Desea registrar esta factura?', parameters, function () {
            location.href = "/compra/listFacturasCompras/"
        });
    });
});

// validar entrada
function validate_form_text(type, event, regex) {
    var key = event.keyCode || event.which;
    var numbers = (key > 47 && key < 58) || key === 8;
    var numbers_spaceless = (key > 47 && key < 58);
    var letters = !((key !== 32) && (key < 65) || (key > 90) && (key < 97) || (key > 122 && key !== 241 && key !== 209 && key !== 225 && key !== 233 && key !== 237 && key !== 243 && key !== 250 && key !== 193 && key !== 201 && key !== 205 && key !== 211 && key !== 218)) || key === 8;
    var letters_spaceless = !((key < 65) || (key > 90) && (key < 97) || (key > 122 && key !== 241 && key !== 209 && key !== 225 && key !== 233 && key !== 237 && key !== 243 && key !== 250 && key !== 193 && key !== 201 && key !== 205 && key !== 211 && key !== 218)) || key === 8;
    var decimals = ((key > 47 && key < 58) || key === 8 || key === 46);

    if (type === 'numbers') {
        return numbers;
    } else if (type === 'letters') {
        return letters;
    } else if (type === 'numbers_letters') {
        return numbers || letters;
    } else if (type === 'letters_spaceless') {
        return letters_spaceless;
    } else if (type === 'letters_numbers_spaceless') {
        return letters_spaceless || numbers_spaceless;
    } else if (type === 'decimals') {
        return decimals;
    } else if (type === 'regex') {
        return regex;
    }
    return true;
}

function add_miles(value){
    return value.toString().replace(/\D/g, "")
                        .replace(/([0-9])([0-9]{3})$/, '$1.$2')
                        .replace(/\B(?=(\d{3})+(?!\d)\.?)/g, ".");
}