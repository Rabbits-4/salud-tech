from flask import Response, request
import json

import anonimacion.seedwork.presentacion.api as api
from anonimacion.modulos.anonimacion.aplicacion.mapeadores import MappeadorDatasetMedicoDTOJson
from anonimacion.modulos.anonimacion.aplicacion.comandos.create_dataset import CreateDatasetMedico
from anonimacion.seedwork.aplicacion.comandos import ejecutar_commando
from anonimacion.seedwork.dominio.excepciones import ExcepcionDominio
import logging

bp = api.crear_blueprint('anonimacion', '/anonimacion')

@bp.route('/test_anonimacion', methods=['GET'])
def test_anonimacion():
    response_body = {
        "message": "Get request processed succesfully"
    }
    return Response(json.dumps(response_body), status=200, mimetype='application/json')

@bp.route('/anonimizar_imagen', methods=['POST'])
def anonimizar_imagen():
    response_body = {
        "message": "Se ha recibido una solicitud para anonimizar una imagen"
    }
    return Response(json.dumps(response_body), status=200, mimetype='application/json')

# @bp.route('/anonimizar_imagen', methods=['POST'])
# def anonimizar_imagen():
#     try:
#         dataset_dict = request.json        
#         map_dataset = MappeadorDatasetMedicoDTOJson()
#         dataset_dto = map_dataset.externo_a_dto(dataset_dict)

#         comando = CreateDatasetMedico(
#             packet_id=dataset_dto.packet_id,
#             entorno_clinico=dataset_dto.entorno_clinico,
#             registro_de_diagnostico=dataset_dto.metadata.registro_de_diagnostico,
#             fecha_creacion=dataset_dto.metadata.fecha_creacion,
#             fecha_actualizacion=dataset_dto.metadata.fecha_actualizacion,
#             historial_paciente_id=dataset_dto.metadata.historial_paciente_id,
#             contexto_procesal=dataset_dto.metadata.contexto_procesal,
#             notas_clinicas=dataset_dto.metadata.notas_clinicas,            
#             data=dataset_dto.data
#         )
        
#         # TODO: use a real dispacher (see dispacher on infraestructure)
#         ejecutar_commando(comando)
        
#         return Response('{}', status=202, mimetype='application/json')
#     except ExcepcionDominio as e:
#         return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')