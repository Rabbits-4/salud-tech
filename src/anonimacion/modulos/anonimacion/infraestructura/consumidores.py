import pulsar, _pulsar  
from pulsar.schema import *  
import logging  
import traceback  

from anonimacion.modulos.anonimacion.infraestructura.schema.v1.eventos import EventoDicomAnonimoCreado  
from anonimacion.seedwork.infraestructura import utils  
from anonimacion.modulos.sagas.aplicacion.comandos.anonimacion import RollbackAnonimacion
from anonimacion.modulos.anonimacion.infraestructura.repositorios import RepositorioDicomAnonimo
from anonimacion.config.db import db

def suscribirse_a_eventos():  
    """
    Se suscribe a eventos normales del sistema.
    """
    cliente = None  
    try:  
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')  
        
        consumidor_eventos = cliente.subscribe(
            'eventos-dicom-anonimo', 
            consumer_type=_pulsar.ConsumerType.Shared,
            subscription_name='anonimacion-sub-eventos',
            schema=AvroSchema(EventoDicomAnonimoCreado)
        )

        while True:  
            mensaje_evento = consumidor_eventos.receive()  
            print(f'[EVENTO] Recibido: {mensaje_evento.value().data}')  

            consumidor_eventos.acknowledge(mensaje_evento)  

        cliente.close()  
    except Exception as e:  
        logging.error(f'ERROR: Suscripción a eventos fallida - {str(e)}')  
        traceback.print_exc()  

def suscribirse_a_rollback():
    """
    Se suscribe al comando de rollback para anonimación.
    """
    cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')

    consumidor = cliente.subscribe(
        'rollback-dicom-anonimo',
        consumer_type=pulsar.ConsumerType.Shared,
        subscription_name='anonimacion-rollback-sub',
        schema=AvroSchema(RollbackAnonimacion)
    )

    while True:
        mensaje = consumidor.receive()
        try:
            evento_rollback = mensaje.value()  # Intentar deserializar
            logging.error(f"🚨 Recibido rollback en anonimación: {evento_rollback}")
            ejecutar_rollback(evento_rollback)
            consumidor.acknowledge(mensaje)
        except Exception as e:
            logging.error(f"❌ Error procesando rollback: {str(e)}")
            logging.error(f"❌ Datos recibidos: {mensaje.data()}")

def ejecutar_rollback(evento):
    """
    Ejecuta la lógica de rollback eliminando el DicomAnonimo de la base de datos.
    """
    repositorio = RepositorioDicomAnonimo()

    # Buscar el DicomAnonimo relacionado al evento
    dicom_a_eliminar = repositorio.obtener_por_id(evento.id_evento)
    
    if dicom_a_eliminar:
        logging.error(f"🗑 Eliminando DicomAnonimo con ID: {evento.id_evento}")
        repositorio.eliminar(evento.id_evento)

        # Confirmar el rollback
        publicar_evento_rollback_completado(evento.id_evento)
    else:
        logging.error(f"⚠ No se encontró DicomAnonimo con ID: {evento.id_evento}")

def publicar_evento_rollback_completado(id_evento):
    """
    Publica un evento confirmando que el rollback en anonimación se ha completado.
    """
    from sagas.dominio.eventos.anonimacion import RollbackAnonimacionCompletado
    from anonimacion.modulos.anonimacion.infraestructura.despachadores import Despachador

    despachador = Despachador()
    evento = RollbackAnonimacionCompletado(id_evento=id_evento)
    
    logging.error(f"✅ Publicando evento de rollback completado: {evento}")
    despachador.publicar_evento(evento, 'rollback-completado')

def suscribirse_a_comandos():
    """
    Se suscribe a comandos del sistema.
    """
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('comandos-dicom-anonimo', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='anonimacion-sub-comandos', schema=AvroSchema(ComandoCrearDicomAnonimo))

        while True:
            mensaje = consumidor.receive()
            print(f'Comando recibido: {mensaje.value().data}')

            consumidor.acknowledge(mensaje)     
            
        cliente.close()
    except:
        logging.error('ERROR: Suscribiéndose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()
