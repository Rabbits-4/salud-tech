from flask import Response, request
import json

import salud_tech.seedwork.presentacion.api as api
from salud_tech.modulos.procesamiento.aplicacion.mapeadores import MappeadorDatasetMedicoDTOJson
from salud_tech.modulos.procesamiento.aplicacion.comandos.create_dataset import CreateDatasetMedico
from salud_tech.seedwork.aplicacion.comandos import ejecutar_commando
from salud_tech.seedwork.dominio.excepciones import ExcepcionDominio
import logging

bp = api.crear_blueprint('procesamiento', '/procesamiento')

@bp.route('/test_procesamiento', methods=['GET'])
def test_procesamiento():
    response_body = {
        "message": "Get request processed succesfully"
    }
    return Response(json.dumps(response_body), status=200, mimetype='application/json')

@bp.route('/crear-dataset-medico-comando', methods=['POST'])
def crear_dataset_medico():
    try:
        dataset_dict = request.json        
        map_dataset = MappeadorDatasetMedicoDTOJson()
        dataset_dto = map_dataset.externo_a_dto(dataset_dict)

        comando = CreateDatasetMedico(
            packet_id=dataset_dto.packet_id,
            entorno_clinico=dataset_dto.entorno_clinico,
            registro_de_diagnostico=dataset_dto.metadata.registro_de_diagnostico,
            fecha_creacion=dataset_dto.metadata.fecha_creacion,
            fecha_actualizacion=dataset_dto.metadata.fecha_actualizacion,
            historial_paciente_id=dataset_dto.metadata.historial_paciente_id,
            contexto_procesal=dataset_dto.metadata.contexto_procesal,
            notas_clinicas=dataset_dto.metadata.notas_clinicas,            
            data=dataset_dto.data
        )
        
        # TODO: use a real dispacher (see dispacher on infraestructure)
        ejecutar_commando(comando)
        
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')