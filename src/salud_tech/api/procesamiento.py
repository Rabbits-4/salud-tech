from flask import Response, request
import aeroalpes.seedwork.presentacion.api as api

bp = api.crear_blueprint('procesamiento', '/procesamiento')

@bp.route('/crear-dataset-medico-comando', methods=('POST'))
def crear_dataset_medico():
    try:
        dataset_dict = request.json

        map_dataset = MapeadorDatasetDTOJson()
        dataset_dto = map_dataset.externo_a_dto(dataset_dict)

        comando = CrearDatasetMedico(dataset_dto.fecha_creacion, dataset_dto.fecha_actualizacion, dataset_dto.id, dataset_dto.pacientes, dataset_dto.medicos, dataset_dto.consultas)        
        
        ejecutar_commando(comando)
        
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')