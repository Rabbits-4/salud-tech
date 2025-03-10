import logging
import pulsar
import os
import datetime
from pulsar.schema import *
from anonimacion.seedwork.infraestructura import utils
from sagas.dominio.eventos.anonimacion import DicomAnonimizadoFallido, AnonimacionIniciada, DicomAnonimizado
from sagas.dominio.eventos.mapeo import DicomMapeoFallido, MapeoIniciado, ParquetCreado
from sagas.dominio.eventos.procesamiento import ProcesamientoFallido, ProcesamientoIniciado, DatasetCreado
from sagas.aplicacion.comandos.anonimacion import RollbackAnonimacion
from sagas.aplicacion.comandos.mapeo import RollbackMapeo
from sagas.aplicacion.comandos.procesamiento import RollbackProcesamiento

class CoordinadorSagaAnonimizacion:
    
    def __init__(self):
        self.cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        self.productor_rollback_anonimacion = self.cliente.create_producer('rollback-dicom-anonimo', schema=AvroSchema(RollbackAnonimacion))
        self.productor_rollback_mapeo = self.cliente.create_producer('rollback-mapeo', schema=AvroSchema(RollbackMapeo))
        self.productor_rollback_procesamiento = self.cliente.create_producer('rollback-procesamiento', schema=AvroSchema(RollbackProcesamiento))

    def configurar_logging(self):
        """ Configura los logs para guardarlos en archivos .log con timestamp """
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_dir = "logs_saga"
        os.makedirs(log_dir, exist_ok=True) 
        log_file = os.path.join(log_dir, f"saga_anonimizacion_{fecha_actual}.log")

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(message)s",
            handlers=[
                logging.FileHandler(log_file, mode="a"),  
                logging.StreamHandler()  
            ]
        )
        
    def suscribirse_a_eventos(self):
        consumidor = self.cliente.subscribe(
            'eventos-saga',
            subscription_name='saga-coordinator-sub',
            schema=AvroSchema(Union[
                AnonimacionIniciada, DicomAnonimizado, 
                MapeoIniciado, ParquetCreado, 
                ProcesamientoIniciado, DatasetCreado,
                DicomAnonimizadoFallido, DicomMapeoFallido, ProcesamientoFallido
            ])
        )

        logging.info("🔥 Iniciando Coordinador de la Saga de Anonimización")

        while True:
            mensaje = consumidor.receive()
            evento = mensaje.value()
            logging.info(f"📡 Evento recibido en Coordinador de Saga: {evento}")

            if isinstance(evento, AnonimacionIniciada):
                self.log_evento("Saga iniciada", evento)

            elif isinstance(evento, DicomAnonimizado):
                self.log_evento("Dicom Anonimizado correctamente", evento)

            elif isinstance(evento, MapeoIniciado):
                self.log_evento("Mapeo Iniciado", evento)

            elif isinstance(evento, ParquetCreado):
                self.log_evento("Parquet Creado correctamente", evento)

            elif isinstance(evento, ProcesamientoIniciado):
                self.log_evento("Procesamiento Iniciado", evento)

            elif isinstance(evento, DatasetCreado):
                self.log_evento("Dataset Creado correctamente", evento)
                logging.info("✅ Termina la saga con éxito.")

            elif isinstance(evento, DicomAnonimizadoFallido):
                self.manejar_fallo_anonimacion(evento)

            elif isinstance(evento, DicomMapeoFallido):
                self.manejar_fallo_mapeo(evento)

            elif isinstance(evento, ProcesamientoFallido):
                self.manejar_fallo_procesamiento(evento)

            consumidor.acknowledge(mensaje)

    def log_evento(self, mensaje, evento):
        """ Registra el estado del proceso en los logs """
        logging.info(f"➡️ {mensaje}: {evento}")

    def manejar_fallo_anonimacion(self, evento):
        logging.error(f"Fallo en Anonimización. Emitiendo rollback: {evento}")
        self.productor_rollback_anonimacion.send(RollbackAnonimacion(id_evento=evento.id_evento))

    def manejar_fallo_mapeo(self, evento):
        logging.error(f"Fallo en Mapeo & Validación. Emitiendo rollback: {evento}")
        self.productor_rollback_mapeo.send(RollbackMapeo(id_evento=evento.id_evento))

    def manejar_fallo_procesamiento(self, evento):
        logging.error(f"Fallo en Procesamiento. Emitiendo rollback: {evento}")
        self.productor_rollback_procesamiento.send(RollbackProcesamiento(id_evento=evento.id_evento))
