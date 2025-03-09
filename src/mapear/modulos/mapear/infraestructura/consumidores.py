import pulsar,_pulsar  
from pulsar.schema import *
import uuid
import time
import logging
import traceback
import requests

from mapear.modulos.mapear.infraestructura.schema.v1.eventos import EventoDicomAnonimoCreado
from mapear.modulos.mapear.infraestructura.schema.v1.comandos import ComandoCrearParquet
from mapear.seedwork.infraestructura import utils
from mapear.modulos.mapear.aplicacion.comandos.create_parquet import CreateParquet

def suscribirse_a_eventos():
    cliente = None
    try:
        print(f'pulsar://{utils.broker_host()}:6650')
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        topico = 'dicom-anonimizado'
        consumidor = cliente.subscribe(
            topico,
            consumer_type=_pulsar.ConsumerType.Shared,subscription_name='dicom-sub',
            schema=AvroSchema(EventoDicomAnonimoCreado)
        )

        while True:
            mensaje = consumidor.receive()
            evento = mensaje.value()
            data = evento.data

            print(f'Evento recibido: {mensaje.value().data}')
            logging.error(f"📡 Evento dicom-anonimizado recibido: {topico}")

            comando = CreateParquet(
                entorno_clinico=data.entorno_clinico,
                registro_de_diagnostico=data.registro_de_diagnostico,
                fecha_creacion=data.fecha_creacion,
                fecha_actualizacion=data.fecha_actualizacion,
                historial_paciente_id=str(uuid.uuid4()),
                contexto_procesal=data.contexto_procesal,
                notas_clinicas=data.notas_clinicas,
                data=data.data
            )

            from mapear.seedwork.aplicacion.comandos import ejecutar_commando

            logging.error("📦 Ejecutar evento: crear parquet")

            ejecutar_commando(comando)

            # requests.post('http://localhost:5002/mapear/create-parquet', json=comando.to_dict())

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