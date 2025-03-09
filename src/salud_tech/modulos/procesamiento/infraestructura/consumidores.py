import pulsar,_pulsar  
from pulsar.schema import *
import uuid
import time
import logging
import traceback
import json

from salud_tech.modulos.procesamiento.infraestructura.schema.v1.eventos import EventoParquetCreado
from salud_tech.modulos.procesamiento.infraestructura.schema.v1.comandos import ComandoCrearDatasetMedico
from salud_tech.seedwork.infraestructura import utils
from salud_tech.modulos.procesamiento.aplicacion.comandos.create_dataset import CreateDatasetMedico
from salud_tech.modulos.procesamiento.aplicacion.handlers import HandlerEventoParquetCreado


def suscribirse_a_eventos():
    """
    Suscripción al evento `parquet-creado` en Pulsar y procesamiento con el Handler de Integración.
    """
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        topico = 'parquet-creado'

        consumidor = cliente.subscribe(
            topico, 
            consumer_type=_pulsar.ConsumerType.Shared,
            subscription_name='salud-tech-sub-eventos', 
            schema=AvroSchema(EventoParquetCreado)
        )
        
        logging.info(f"✅ [Procesamiento] Suscripción exitosa al tópico `{topico}`.")
        handler = HandlerEventoParquetCreado()

        while True:
            mensaje = consumidor.receive()
            evento = mensaje.value()

            try:
                registro_de_diagnostico = json.loads(evento.data.registro_de_diagnostico.replace("'", "\""))
                data = json.loads(evento.data.data.replace("'", "\""))
            except json.JSONDecodeError:
                registro_de_diagnostico = evento.data.registro_de_diagnostico
                data = evento.data.data
                logging.warning("⚠ [MAPEO] Los datos no están en formato JSON válido, se mantendrán como strings.")

            datos_evento = {
                "packet_id": evento.data.packet_id,
                "entorno_clinico": evento.data.entorno_clinico,
                "registro_de_diagnostico": registro_de_diagnostico,
                "fecha_creacion": evento.data.fecha_creacion,
                "fecha_actualizacion": evento.data.fecha_actualizacion,
                "historial_paciente_id": evento.data.historial_paciente_id,
                "contexto_procesal": evento.data.contexto_procesal,
                "notas_clinicas": evento.data.notas_clinicas,
                "data": data
            }

            handler.handle(datos_evento)   

            consumidor.acknowledge(mensaje)     

        cliente.close()
    except:
        traceback.print_exc()
        if cliente:
            cliente.close()

def suscribirse_a_comandos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('comandos-dataset-medico', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='salud-tech-sub-comandos', schema=AvroSchema(ComandoCrearDatasetMedico))

        while True:
            mensaje = consumidor.receive()
            print(f'Comando recibido: {mensaje.value().data}')

            consumidor.acknowledge(mensaje)     
            
        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()