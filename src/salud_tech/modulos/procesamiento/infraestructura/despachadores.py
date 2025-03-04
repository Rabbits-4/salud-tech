import pulsar
from pulsar.schema import *

from salud_tech.modulos.procesamiento.infraestructura.schema.v1.eventos import EventoDatasetMedicoCreado, DatasetMedicoCreadoPayload
from salud_tech.modulos.procesamiento.infraestructura.schema.v1.comandos import ComandoCrearDatasetMedico, ComandoCrearDatasetMedicoPayload
from salud_tech.seedwork.infraestructura import utils

import datetime
import logging

epoch = datetime.datetime.utcfromtimestamp(0)

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

class Despachador:
    def _publicar_mensaje(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=AvroSchema(EventoDatasetMedicoCreado))
        publicador.send(mensaje)
        cliente.close()

    def publicar_evento(self, evento, topico):
        # TODO Debe existir un forma de crear el Payload en Avro con base al tipo del evento
        logging.error("***** publish", evento)
        payload = DatasetMedicoCreadoPayload(
            id_dataset_medico=str(evento.id), 
            fecha_creacion=int(unix_time_millis(evento.fecha_creacion))
        )
        evento_integracion = EventoDatasetMedicoCreado(data=payload)
        self._publicar_mensaje(evento_integracion, topico, AvroSchema(EventoDatasetMedicoCreado))

    def publicar_comando(self, comando, topico):
        # TODO Debe existir un forma de crear el Payload en Avro con base al tipo del comando
        payload = ComandoCrearDatasetMedicoPayload(
            packet_id=str(comando.packet_id)            
        )
        comando_integracion = ComandoCrearDatasetMedico(data=payload)
        self._publicar_mensaje(comando_integracion, topico, AvroSchema(ComandoCrearDatasetMedico))
