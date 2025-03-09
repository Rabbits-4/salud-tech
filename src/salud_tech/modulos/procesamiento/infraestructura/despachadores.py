import pulsar
from pulsar.schema import *

from salud_tech.modulos.procesamiento.infraestructura.schema.v1.eventos import (
    EventoDatasetMedicoCreado, DatasetMedicoCreadoPayload,
    ProcesamientoIniciado, ProcesamientoIniciadoPayload
)
from salud_tech.modulos.procesamiento.infraestructura.schema.v1.comandos import ComandoCrearDatasetMedico, ComandoCrearDatasetMedicoPayload
from salud_tech.seedwork.infraestructura import utils

import datetime
import logging

epoch = datetime.datetime.utcfromtimestamp(0)

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

class Despachador:
    def _publicar_mensaje(self, mensaje, topico, schema):
        try:
            cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
            publicador = cliente.create_producer(topico, schema=AvroSchema(schema)) 
            publicador.send(mensaje)
            logging.info(f"📡 Mensaje enviado a `{topico}` exitosamente.")
        except Exception as e:
            logging.error(f"❌ Error publicando mensaje en `{topico}`: {e}")
        finally:
            cliente.close()

    def publicar_evento(self, evento, topico):
        # TODO Debe existir un forma de crear el Payload en Avro con base al tipo del evento
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

    def publicar_evento_saga(self, evento, topico="eventos-saga"):
        """ Publica eventos en el broker Pulsar. """
        payload = ProcesamientoIniciadoPayload(
            id_saga=str(evento.id_saga),
            paso=str(evento.paso)
        )
        evento_a_publicar = ProcesamientoIniciado(data=payload)
        topico = "eventos-saga"

        logging.info(f"✅ Publicando evento `{evento.__class__.__name__}` en `{topico}`.")
        self._publicar_mensaje(evento_a_publicar, topico, evento_a_publicar.__class__)