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
            dict.subtotal = dict.cantidad * parseFloat(dict.precio);
            subtotal += dict.subtotal;
        })
        this.items.total_factura = Math.round(subtotal);
        this.items.total_iva = Math.round(subtotal/11);
        $('#totalIva').val(this.items.total_iva); // el iva en el template
        $('#total').val(this.items.total_factura); // para el total
    },
    add: function (item) {
        this.items.products.push(item);
        this.list();
    },
    list: function () {
        this.calc_invoice()
        tblFactura = $('#tblFactura').DataTable({
            responsive: true,
            destroy: true,
            data: this.items.products,
            ordering: false,
            columns: [
                {"data": "codigo_producto"},
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
                    width: "30%",
                    orderable: false,                
                },
                {
                    targets: [2, 4],
                    class: "text-center my-0 ",
                    orderable: false,
                    render: function (data, type, row) {
                        return 'Gs. ' + parseFloat(data);
                    }
                },
                {
                    targets: [3],
                    width: "20%",
                    class: "text-center",
                    orderable: false,  
                    render: function (data, type, row) {
                        if(action == "A"){
                            if(row.cantidad_pedido === "-"){
                                return '<input type="text" name="cantidad" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.cantidad + '">';
                            }else{
                                return '<input type="text" name="cantidad" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.cantidad_pedido + '">';
                            }    
                        }else{  
                            return '<input type="text" name="cantidad" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.cantidad_pedido + '">';
                        }                                            
                    }                 
                },
                {
                    targets: [5],
                    class: "text-center",
                    width: "5%",
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger m-0 p-0"><i class="fa fa-trash m-1" style="color: white" aria-hidden="true"></i>\n</i></a>'
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
        console.clear();
        var cant = parseInt($(this).val());
        var tr = tblFactura.cell($(this).closest('td, li')).index();
        factura.items.products[tr.row].cantidad = cant;
        factura.calc_invoice();
        // el 4 es el lugar donde tiene que estar el subtotal
        $('td:eq(4)', tblFactura.row(tr.row).node()).html('Gs.' + Math.round(factura.items.products[tr.row].subtotal));
        console.log(cant);
    }).on('change', 'input[name="descripcion"]', function (){
        var descripcion = $(this).val();
        var tr = tblFactura.cell($(this).closest('td, li')).index();
        factura.items.products[tr.row].description = descripcion;
    });

    $('form').on('submit', function (e) {
        e.preventDefault();
        factura.items.proveedor = $('select[name="id_proveedor"]').val();
        console.log(factura.items.proveedor)
        factura.items.fecha_emision = $('input[name="fecha_emision"]').val();
        console.log(factura.items.fecha_emision)
        factura.items.fecha_vencimiento = $('input[name="fecha_vencimiento"]').val();
        console.log(factura.items.fecha_vencimiento)
        factura.items.nro_factura = $('input[name="nro_factura"]').val();
        console.log(factura.items.nro_factura)
        factura.items.nro_timbrado = $('input[name="nro_timbrado"]').val();
        console.log(factura.items.nro_timbrado)
        var parameters = new FormData();
        console.log(factura.items)
        parameters.append('factura', JSON.stringify(factura.items));
        var csrf = $('input[name="csrfmiddlewaretoken"]').val();
        parameters.append('csrfmiddlewaretoken', csrf);
        console.log(parameters)
        submit_with_ajax(window.location.pathname, 'Noticicación', '¿Desea registrar esta factura?', parameters, function () {
            location.href = "/compra/addFacturaCompra/"
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