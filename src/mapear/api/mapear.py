from flask import Response, request
import json

import mapear.seedwork.presentacion.api as api
from mapear.modulos.mapear.aplicacion.mapeadores import MappeadorParquetDTOJson
from mapear.modulos.mapear.aplicacion.comandos.create_parquet import CreateParquet
from mapear.seedwork.aplicacion.comandos import ejecutar_commando
from mapear.seedwork.dominio.excepciones import ExcepcionDominio
import logging

bp = api.crear_blueprint('mapear', '/mapear')

@bp.route('/test_mapear', methods=['GET'])
def test_procesamiento():
    response_body = {
        "message": "Get request processed succesfully"
    }
    return Response(json.dumps(response_body), status=200, mimetype='application/json')

@bp.route('/create-parquet', methods=['POST'])
def crear_parquet():
    try:
        dataset_dict = request.json
        map_dataset = MappeadorParquetDTOJson()
        dataset_dto = map_dataset.externo_a_dto(dataset_dict)

        comando = CreateParquet(
            entorno_clinico=dataset_dto.entorno_clinico,
            registro_de_diagnostico=dataset_dto.registro_de_diagnostico,
            fecha_creacion=dataset_dto.fecha_creacion,
            fecha_actualizacion=dataset_dto.fecha_actualizacion,
            historial_paciente_id=dataset_dto.historial_paciente_id,
            contexto_procesal=dataset_dto.contexto_procesal,
            notas_clinicas=dataset_dto.notas_clinicas,            
            data=dataset_dto.data
        )
        
        # TODO: use a real dispacher (see dispacher on infraestructure)
        ejecutar_commando(comando)
        
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')