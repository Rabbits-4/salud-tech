import pulsar
from pulsar.schema import *

from mapear.modulos.mapear.infraestructura.schema.v1.eventos import EventoParquetCreado, ParquetCreadoPayload
from mapear.modulos.mapear.infraestructura.schema.v1.comandos import ComandoCrearParquet, ComandoCrearParquetPayload
from mapear.seedwork.infraestructura import utils

import datetime
import logging

epoch = datetime.datetime.utcfromtimestamp(0)

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

class Despachador:
    def _publicar_mensaje(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=AvroSchema(EventoParquetCreado))
        publicador.send(mensaje)
        cliente.close()

    def publicar_evento(self, evento, topico):
        # TODO Debe existir un forma de crear el Payload en Avro con base al tipo del evento
        logging.error("***", evento)
        logging.error("*** topico", topico)
        payload = ParquetCreadoPayload(
            id_parquet=str(evento.id),
            entorno_clinico=evento.entorno_clinico,
            registro_de_diagnostico=evento.registro_de_diagnostico,

        )
        evento_integracion = EventoParquetCreado(data=payload)
        self._publicar_mensaje(evento_integracion, topico, AvroSchema(EventoParquetCreado))

    def publicar_comando(self, comando, topico):
        # TODO Debe existir un forma de crear el Payload en Avro con base al tipo del comando
        payload = ComandoCrearParquetPayload(
            packet_id=str(comando.packet_id)            
        )
        comando_integracion = ComandoCrearParquet(data=payload)
        self._publicar_mensaje(comando_integracion, topico, AvroSchema(ComandoCrearParquet))
