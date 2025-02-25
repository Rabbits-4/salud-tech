import salud_tech.seedwork.presentacion.api as api

bp = api.crear_blueprint('procesamiento', '/procesamiento')

@bp.route('/procesar-dataset', methods=('POST',))
def handle_procesar_dataset():
    ...
