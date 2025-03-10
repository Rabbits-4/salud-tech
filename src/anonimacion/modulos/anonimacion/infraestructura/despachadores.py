import pulsar  
from pulsar.schema import *  
import datetime  
import logging  

from anonimacion.modulos.anonimacion.infraestructura.schema.v1.eventos import (
    EventoDicomAnonimoCreado, DicomAnonimoCreadoPayload,
    AnonimacionIniciada, AnonimacionIniciadaPayload
)
from anonimacion.seedwork.infraestructura import utils  

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

    def publicar_evento(self, evento, topico="dicom-anonimizado"):
        payload = DicomAnonimoCreadoPayload(
            id_dicom_anonimo=str(evento.id),
            imagen=evento.imagen,
            entorno_clinico=evento.entorno_clinico,
            registro_de_diagnostico=str(evento.registro_de_diagnostico),
            fecha_creacion=str(evento.fecha_creacion),
            fecha_actualizacion=str(evento.fecha_actualizacion),
            contexto_procesal=evento.contexto_procesal,
            notas_clinicas=evento.notas_clinicas,
            data=str(evento.data)
        )
        evento_a_publicar = EventoDicomAnonimoCreado(data=payload)
        topico = "dicom-anonimizado"            
        logging.info(f"✅ Publicando evento `{evento.__class__.__name__}` en `{topico}`.")
        self._publicar_mensaje(evento_a_publicar, topico, evento_a_publicar.__class__)

    def publicar_evento_saga(self, evento, topico="eventos-saga"):
        """ Publica eventos en el broker Pulsar. """
        payload = AnonimacionIniciadaPayload(
            id_saga=str(evento.id_saga),
            paso=str(evento.paso)
        )
        evento_a_publicar = AnonimacionIniciada(data=payload)
        topico = "eventos-saga"

        logging.info(f"✅ Publicando evento `{evento.__class__.__name__}` en `{topico}`.")
        self._publicar_mensaje(evento_a_publicar, topico, evento_a_publicar.__class__)