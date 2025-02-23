import aeroalpes.seedwork.presentacion.api as api

bp = api.crear_blueprint('procesamiento', '/procesamiento')

@bp.route('/reserva-comando', methods=('POST',))
def hanble_imagen():
    ...