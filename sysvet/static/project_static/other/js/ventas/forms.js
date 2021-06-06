var tblFactura;

// Estructura para el detalle de facturas
var factura = {
    items: {
        cliente: '',
        nro_factura: '',
        nro_timbrado: '',
        total_iva: 0,
        total_factura: 0,
        products: []
    },
    calc_invoice: function () {
        var subtotal = 0
        $.each(this.items.products, function (pos, dict) {
            var dic_precio_format = dict.precio.split('.')
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
        tblFactura = $('#tblFacturaVenta').DataTable({
            responsive: true,
            destroy: true,
            data: this.items.products,
            ordering: false,
            columns: [
                {"data": "codigo_producto"},
                {"data": "nombre"},
                {"data": "description"},
                {"data": "precio"},
                {"data": "cantidad"},
                {"data": "subtotal"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: "text-center",
                    width: "10%",
                    orderable: false,
                },
                
                {
                    targets: [1],
                    class: "",
                    width: "20%",
                    orderable: false,                
                },
                {
                    targets: [2],
                    class: "",
                    width: "20%",
                    orderable: false,                
                },
                {
                    targets: [3, 5],
                    class: "text-center my-0 ",
                    width: "15%",
                    orderable: false,
                    render: function (data, type, row) {
                        var amount_formated = add_miles(data)
                        return 'Gs. ' + amount_formated
                    }
                },
                {
                    targets: [4],
                    width: "15%",
                    class: "text-center",
                    orderable: false,  
                    render: function (data, type, row) {
                        if(action === "A"){
                            return '<input type="text" name="cantidad" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.cantidad + '">';
                        }else{
                            return row.cantidad;
                        }
                    }            
                },
                {
                    targets: [6],
                    class: "text-center",
                    width: "5%",
                    orderable: false,
                    render: function (data, type, row) {
                        if(action === "A"){
                            return '<a rel="remove" class="btn btn-danger m-0 p-0"><i class="fa fa-trash m-1" style="color: white" aria-hidden="true"></i>\n</i></a>'
                        }
                        else{
                            return "-"
                        }
                    }
                },
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
                infoEmpty: "Mostrando 0 to 0 de 0 Entradas",
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

        data['cantidad'] = 1
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

    $('#tblFacturaVenta').on('click', 'a[rel="remove"]', function () {
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
    });

    $('form').on('submit', function (e) {
        if(factura.items.products.length == 0){
            swal({
                title: "Notificación",
                text: "Debe cargar al menos un producto para el pedido!",
                icon: "warning",
                button: "Ok",
            })
            e.preventDefault();
        }else{
            e.preventDefault();
            factura.items.cliente = $('select[name="id_cliente"]').val();
            factura.items.nro_factura = $('input[name="nro_factura"]').val();
            factura.items.nro_timbrado = $('input[name="nro_timbrado"]').val();
            var parameters = new FormData();
            parameters.append('factura', JSON.stringify(factura.items));
            var csrf = $('input[name="csrfmiddlewaretoken"]').val();
            parameters.append('csrfmiddlewaretoken', csrf);
            submit_with_ajax(window.location.pathname, 'Noticicación', '¿Desea registrar esta factura?', parameters, function () {
                location.href = "/factura/listFacturasVentas/"
            });
        }
        
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