function abrir_modal_edicion(url) {
	$('#edicion').load(url, function () {
		$(this).modal('show');
	});
}
function abrir_modal_creacion(url) {
	$('#creacion').load(url, function () {
		$(this).modal('show');
	});
}
function abrir_modal_eliminacion(url) {
	$('#eliminacion').load(url, function () {
		$(this).modal('show');
	});
}
function cerrar_modal_creacion(){
	$('#creacion').modal('hide');
}

function cerrar_modal_edicion() {
	$('#edicion').modal('hide');
}
function cerrar_modal_eliminacion() {
	$('#eliminacion').modal('hide');
}

function replaceCaratect(e) {
	e.value = e.value.replace(/[^A-Za-zÀ-ÿ\u00f1\u00d1\s-]+$/g, '')
}

function replaceABC(e) {
	e.value = e.value.replace(/[^0-9-]/g, '')
}

function replaceDirection(e) {
	e.value = e.value.replace(/[^A-Za-zÀ-ÿ0-9\u00f1\u00d1\s-]+$/g, '')
}
