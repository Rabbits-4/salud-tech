from flask import Response, request
import json

import mapear.seedwork.presentacion.api as api
from mapear.modulos.mapear.aplicacion.mapeadores import MappeadorParquetDTOJson, MapeadorParquet
from mapear.modulos.mapear.aplicacion.comandos.create_parquet import CreateParquet
from mapear.modulos.mapear.aplicacion.queries.obtener_todos_parquets import ObtenerParquets
from mapear.seedwork.aplicacion.comandos import ejecutar_commando
from mapear.seedwork.aplicacion.queries import ejecutar_query
from mapear.seedwork.dominio.excepciones import ExcepcionDominio
import logging

bp = api.crear_blueprint('mapear', '/mapear')

@bp.route('/test_mapear', methods=['GET'])
def test_mapear():
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

@bp.route('/obtener-parquets', methods=['GET'])
def get_parquets():
    query = ObtenerParquets()
    resultado = ejecutar_query(query).resultado

    parquet_mapeador = MapeadorParquet()
    mapeador_json = MappeadorParquetDTOJson()
    
    resultado_dto = [parquet_mapeador.entidad_a_dto(parquet) for parquet in resultado]
    resultado_externo = [mapeador_json.dto_a_externo(parquet) for parquet in resultado_dto]

    json_response = json.dumps(resultado_externo, default=str)

    return Response(json_response, status=200, mimetype='application/json')

