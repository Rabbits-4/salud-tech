import pulsar
from pulsar.schema import *

from salud_tech.modulos.procesamiento.infraestructura.schema.v1.eventos import EventoDatasetCreado, DatasetCreadoPayload
from salud_tech.modulos.procesamiento.infraestructura.schema.v1.comandos import ComandoCrearDataset, ComandoCrearDatasetPayload
from salud_tech.seedwork.infraestructura import utils

import datetime

epoch = datetime.datetime.utcfromtimestamp(0)

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

class Despachador:
    def _publicar_mensaje(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=AvroSchema(EventoDatasetCreado))
        publicador.send(mensaje)
        cliente.close()

    def publicar_evento(self, evento, topico):
        payload = DatasetCreadoPayload(
            id_dataset=str(evento.id_dataset), 
            estado=str(evento.estado), 
            fecha_creacion=int(unix_time_millis(evento.fecha_creacion))
        )
        evento_integracion = EventoDatasetCreado(data=payload)
        self._publicar_mensaje(evento_integracion, topico, AvroSchema(EventoDatasetCreado))

    def publicar_comando(self, comando, topico):
        payload = ComandoCrearDatasetPayload(
            id_usuario=str(comando.id_usuario)
        )
        comando_integracion = ComandoCrearDataset(data=payload)
        self._publicar_mensaje(comando_integracion, topico, AvroSchema(ComandoCrearDataset))
