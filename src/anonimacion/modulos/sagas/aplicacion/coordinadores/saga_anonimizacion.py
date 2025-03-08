import logging
import pulsar
from pulsar.schema import *
from anonimacion.seedwork.infraestructura import utils
from sagas.dominio.eventos.anonimacion import DicomAnonimizadoFallido
from sagas.dominio.eventos.mapeo import DicomMapeoFallido
from sagas.dominio.eventos.procesamiento import ProcesamientoFallido
from sagas.aplicacion.comandos.anonimacion import RollbackAnonimacion
from sagas.aplicacion.comandos.mapeo import RollbackMapeo
from sagas.aplicacion.comandos.procesamiento import RollbackProcesamiento

class CoordinadorSagaAnonimizacion:
    
    def __init__(self):
        self.cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        self.productor_rollback_anonimacion = self.cliente.create_producer('rollback-dicom-anonimo', schema=AvroSchema(RollbackAnonimacion))
        self.productor_rollback_mapeo = self.cliente.create_producer('rollback-mapeo', schema=AvroSchema(RollbackMapeo))
        self.productor_rollback_procesamiento = self.cliente.create_producer('rollback-procesamiento', schema=AvroSchema(RollbackProcesamiento))
        
    def suscribirse_a_eventos(self):
        consumidor = self.cliente.subscribe(
            'eventos-saga',
            subscription_name='saga-coordinator-sub',
            schema=AvroSchema(Union[DicomAnonimizadoFallido, DicomMapeoFallido, ProcesamientoFallido])
        )

        while True:
            mensaje = consumidor.receive()
            evento = mensaje.value()
            logging.error(f"📡 Evento recibido en Coordinador de Saga: {evento}")

            if isinstance(evento, DicomAnonimizadoFallido):
                self.manejar_fallo_anonimacion(evento)
            elif isinstance(evento, DicomMapeoFallido):
                self.manejar_fallo_mapeo(evento)
            elif isinstance(evento, ProcesamientoFallido):
                self.manejar_fallo_procesamiento(evento)

            consumidor.acknowledge(mensaje)

    def manejar_fallo_anonimacion(self, evento):
        logging.error(f"Fallo en Anonimización. Emitiendo rollback: {evento}")
        self.productor_rollback_anonimacion.send(RollbackAnonimacion(id_evento=evento.id_evento))

    def manejar_fallo_mapeo(self, evento):
        logging.error(f"Fallo en Mapeo & Validación. Emitiendo rollback: {evento}")
        self.productor_rollback_mapeo.send(RollbackMapeo(id_evento=evento.id_evento))

    def manejar_fallo_procesamiento(self, evento):
        logging.error(f"Fallo en Procesamiento. Emitiendo rollback: {evento}")
        self.productor_rollback_procesamiento.send(RollbackProcesamiento(id_evento=evento.id_evento))
