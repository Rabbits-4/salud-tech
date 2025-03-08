import pulsar,_pulsar  
from pulsar.schema import *
import uuid
import time
import logging
import traceback

from mapear.modulos.mapear.infraestructura.schema.v1.eventos import EventoParquetCreado
from mapear.modulos.mapear.infraestructura.schema.v1.comandos import ComandoCrearParquet
from mapear.seedwork.infraestructura import utils

def suscribirse_a_eventos():
    cliente = None
    try:
        print(f'pulsar://{utils.broker_host()}:6650')
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-dataset-medico', consumer_type=_pulsar.ConsumerType.Shared,subscription_name='salud-tech-sub-eventos', schema=AvroSchema(EventoParquetCreado))

        while True:
            mensaje = consumidor.receive()
            print(f'Evento recibido: {mensaje.value().data}')

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
        consumidor = cliente.subscribe('comandos-dataset-medico', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='salud-tech-sub-comandos', schema=AvroSchema(ComandoCrearParquet))

        while True:
            mensaje = consumidor.receive()
            print(f'Comando recibido: {mensaje.value().data}')

            consumidor.acknowledge(mensaje)     
            
        cliente.close()
    except:
        traceback.print_exc()
        if cliente:
            cliente.close()