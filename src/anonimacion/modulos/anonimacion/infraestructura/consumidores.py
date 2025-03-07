import pulsar, _pulsar  
from pulsar.schema import *  
import logging  
import traceback  

from anonimacion.modulos.anonimacion.infraestructura.schema.v1.eventos import EventoDicomAnonimoCreado  
from anonimacion.modulos.anonimacion.infraestructura.schema.v1.comandos import ComandoCrearDicomAnonimo
from anonimacion.seedwork.infraestructura import utils  

def suscribirse_a_eventos():  
    cliente = None  
    try:  
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')  
        
        # Suscripción al tópico de rollback
        consumidor_rollback = cliente.subscribe(
            'rollback-dicom-anonimo', 
            consumer_type=_pulsar.ConsumerType.Shared,
            subscription_name='anonimacion-sub-rollback',
            schema=AvroSchema(EventoDicomAnonimoCreado)
        )

        while True:  
            mensaje_rollback = consumidor_rollback.receive()  
            print(f'[ROLLBACK] Evento recibido: {mensaje_rollback.value().data}')  

            # Procesar rollback
            procesar_rollback(mensaje_rollback.value().data)  

            consumidor_rollback.acknowledge(mensaje_rollback)  

        cliente.close()  
    except Exception as e:  
        logging.error(f'ERROR: Suscripción fallida - {str(e)}')  
        traceback.print_exc()  

def suscribirse_a_comandos():
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
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()

def procesar_rollback(evento_data):  
    # \"\"\"
    # Lógica de compensación para rollback de DicomAnonimo.
    # Puede incluir actualización o eliminación de registros en la base de datos.
    # \"\"\"
    print(f'[ROLLBACK] Procesando evento de rollback para DicomAnonimo con ID {evento_data.get("id_dicom_anonimo")}')

    # Aquí se agregaría la lógica de actualización o eliminación en la base de datos.
    # Por ejemplo, si se necesita eliminar:
    # repositorio.eliminar_por_id(evento_data.get("id_dicom_anonimo"))