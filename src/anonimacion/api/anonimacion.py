from flask import Response, request
import json

import anonimacion.seedwork.presentacion.api as api
from anonimacion.modulos.anonimacion.aplicacion.mapeadores import MapeadorDicomAnonimoDTOJson
from anonimacion.modulos.anonimacion.aplicacion.comandos.anonimizar import Anonimizar
from anonimacion.seedwork.aplicacion.comandos import ejecutar_commando
from anonimacion.seedwork.dominio.excepciones import ExcepcionDominio
import logging

bp = api.crear_blueprint('anonimacion', '/anonimacion')

@bp.route('/test_anonimacion', methods=['GET'])
def test_anonimacion():
    response_body = {
        "message": "Get request processed successfully"
    }
    return Response(json.dumps(response_body), status=200, mimetype='application/json')

@bp.route('/anonimizar_imagen', methods=['POST'])
def anonimizar_imagen():
    try:
        # Obtener el JSON del request
        request_data = request.json
        logging.info(f"Request recibido: {json.dumps(request_data, indent=2)}")

        # Mapear el request a DTO
        mapeador = MapeadorDicomAnonimoDTOJson()
        dicom_dto = mapeador.externo_a_dto(request_data)

        comando = Anonimizar(
            historial_paciente_id=dicom_dto.historial_paciente_id,
            nombre_paciente=dicom_dto.nombre_paciente,
            direccion_paciente=dicom_dto.direccion_paciente,
            telefono_paciente=dicom_dto.telefono_paciente,
            img=dicom_dto.imagen,
            entorno_clinico=dicom_dto.entorno_clinico,
            registro_de_diagnostico=dicom_dto.registro_de_diagnostico,
            fecha_creacion=dicom_dto.fecha_creacion,
            fecha_actualizacion=dicom_dto.fecha_actualizacion,
            contexto_procesal=dicom_dto.contexto_procesal,
            notas_clinicas=dicom_dto.notas_clinicas,
            data=dicom_dto.data
        )

        ejecutar_commando(comando)

        # Responder con el DTO recibido (solo para debug)
        response_body = {
            "message": "Se ha recibido la solicitud correctamente",
            "datos_recibidos": request_data
        }
        return Response(json.dumps(response_body), status=200, mimetype='application/json')

    except ExcepcionDominio as e:
        logging.error(f"Error en el procesamiento: {str(e)}")
        return Response(json.dumps({"error": str(e)}), status=400, mimetype='application/json')

    except Exception as e:
        logging.error(f"Error inesperado: {str(e)}")
        return Response(json.dumps({"error": "Error interno en el servidor"}), status=500, mimetype='application/json')