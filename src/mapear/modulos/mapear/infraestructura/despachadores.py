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
        try:
            cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
            publicador = cliente.create_producer(topico, schema=AvroSchema(schema)) 
            publicador.send(mensaje)
            logging.info(f"📡 Mensaje enviado a `{topico}` exitosamente.")
        except Exception as e:
            logging.error(f"❌ Error publicando mensaje en `{topico}`: {e}")
        finally:
            cliente.close()

    def publicar_evento(self, evento, topico="parquet-creado"):
        payload = ParquetCreadoPayload(
            packet_id=str(evento.id),
            fecha_creacion=str(evento.fecha_creacion),
            fecha_actualizacion=str(evento.fecha_actualizacion),
            registro_de_diagnostico=evento.registro_de_diagnostico,
            entorno_clinico=evento.entorno_clinico or "XXX",
            historial_paciente_id=evento.historial_paciente_id,
            contexto_procesal=evento.contexto_procesal,
            notas_clinicas=evento.notas_clinicas,
            data=evento.data,
            estado=evento.estado
        )
        evento_integracion = EventoParquetCreado(data=payload)
        logging.info(f"✅ Publicando evento `{evento.__class__.__name__}` en `{topico}`.")
        self._publicar_mensaje(evento_integracion, topico, EventoParquetCreado) 

    def publicar_comando(self, comando, topico):
        payload = ComandoCrearParquetPayload(
            packet_id=str(comando.packet_id)            
        )
        comando_integracion = ComandoCrearParquet(data=payload)
        logging.info(f"📢 Publicando comando `{comando.__class__.__name__}` en `{topico}`.")
        self._publicar_mensaje(comando_integracion, topico, ComandoCrearParquet)  
