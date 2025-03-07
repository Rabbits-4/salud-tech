import pulsar  
from pulsar.schema import *  
import datetime  
import logging  

from anonimacion.modulos.anonimacion.infraestructura.schema.v1.eventos import EventoDicomAnonimoCreado, DicomAnonimoCreadoPayload  
from anonimacion.seedwork.infraestructura import utils  

epoch = datetime.datetime.utcfromtimestamp(0)  

def unix_time_millis(dt):  
    return (dt - epoch).total_seconds() * 1000.0  

class Despachador:  
    def _publicar_mensaje(self, mensaje, topico, schema):  
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')  
        publicador = cliente.create_producer(topico, schema=AvroSchema(schema))  
        publicador.send(mensaje)  
        cliente.close()  

    def publicar_evento(self, evento, topico="dicom-anonimizado"):  
        logging.error(f"📡 Intentando publicar evento en el tópico: {topico}")
        # \"\"\"
        # Publica un evento con la información del DicomAnonimo anonmizado.  
        # \"\"\"  
        logging.error("📦 Creando payload del evento")
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
        logging.error("✅ Evento creado, enviando a Pulsar")
        evento_a_publicar = EventoDicomAnonimoCreado(data=payload)  

        self._publicar_mensaje(evento_a_publicar, topico, EventoDicomAnonimoCreado)