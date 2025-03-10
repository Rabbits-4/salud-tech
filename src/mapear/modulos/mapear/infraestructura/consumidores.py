import pulsar,_pulsar  
from pulsar.schema import *
import uuid
import time
import logging
import traceback
import requests
import json

from mapear.modulos.mapear.infraestructura.schema.v1.eventos import EventoDicomAnonimoCreado
from mapear.modulos.mapear.infraestructura.schema.v1.comandos import ComandoCrearParquet
from mapear.seedwork.infraestructura import utils
from mapear.modulos.mapear.aplicacion.comandos.create_parquet import CreateParquet
from mapear.modulos.mapear.aplicacion.handlers import HandlerEventoDicomAnonimizado


def suscribirse_a_eventos():
    """
    Suscripción al evento `dicom-anonimizado` en Pulsar y procesamiento con el Handler de Integración.
    """
    cliente = None
    try: 
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        topico = 'dicom-anonimizado'
        
        consumidor = cliente.subscribe(
            topico,
            consumer_type=_pulsar.ConsumerType.Shared,
            subscription_name='dicom-sub',
            schema=AvroSchema(EventoDicomAnonimoCreado)
        )

        logging.info(f"✅ [MAPEO] Suscripción exitosa al tópico `{topico}`.")
        handler = HandlerEventoDicomAnonimizado()  # 🔹 Creamos una instancia del Handler

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
            

            

            # 🔹 Creamos un objeto limpio con los datos transformados
            datos_evento = {
                "id_dicom_anonimo": evento.data.id_dicom_anonimo,
                "imagen": evento.data.imagen,
                "entorno_clinico": evento.data.entorno_clinico, # it isn't save on db
                "registro_de_diagnostico": registro_de_diagnostico, # dict
                "fecha_creacion": evento.data.fecha_creacion,
                "fecha_actualizacion": evento.data.fecha_actualizacion,
                "contexto_procesal": evento.data.contexto_procesal,
                "notas_clinicas": evento.data.notas_clinicas,
                "data": data #dict
            } 
            
            handler.handle(datos_evento)
            consumidor.acknowledge(mensaje)

    except Exception as e:
        logging.error(f"❌ [MAPEO] Error en la suscripción a `{topico}`: {str(e)}")
        traceback.print_exc()
    
    finally:
        if cliente:
            cliente.close()
            logging.info("🔌 [MAPEO] Cliente de Pulsar cerrado correctamente.")

def suscribirse_a_comandos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('dicom-anonimo', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='mapear-sub-comandos', schema=AvroSchema(ComandoCrearParquet))

        while True:
            mensaje = consumidor.receive()
            print(f'Comando recibido: {mensaje.value().data}')

            consumidor.acknowledge(mensaje)     
            
        cliente.close()
    except:
        traceback.print_exc()
        if cliente:
            cliente.close()