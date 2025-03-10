import os
import time
import logging
import datetime
import pulsar
from pulsar.schema import *

def configurar_logging():
    """ Configura los logs para guardarlos en archivos .log con timestamp """
    try:
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_dir = "logs_saga"
        os.makedirs(log_dir, exist_ok=True)  # Crea la carpeta si no existe
        log_file = os.path.join(log_dir, f"saga_anonimizacion_{fecha_actual}.log")

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(message)s",
            handlers=[
                logging.FileHandler(log_file, mode="a"),  
                logging.StreamHandler()  
            ]
        )
    except Exception as e:
        print(f"Error al configurar logging: {e}")

def main():
    configurar_logging()
    logging.info("El contenedor está funcionando correctamente.")

    logging.info("Configurando pulsar")
    broker_host = os.getenv('PULSAR_ADDRESS', default="broker")
    client = pulsar.Client(f'pulsar://{broker_host}:6650')  
    consumer = client.subscribe('eventos-saga', subscription_name='sagas_sub')
    
    logging.info("Recibiendo mensajes")
    try:
        while True:
            msg = consumer.receive()
            logging.info("Recibido: %s", msg.data().decode('utf-8'))
            consumer.acknowledge(msg)
    except KeyboardInterrupt:
        pass
    finally:
        client.close()

if __name__ == '__main__':
    main()