import os
import logging
import datetime
import re
import pulsar
from pulsar.schema import *

# Variables para rastrear la saga activa
saga_id_global = None
estado_actual_global = None

# Diccionario con el flujo de eventos esperados en la saga
FLUJO_ESPERADO = {
    "anonimacioniniciada": "dicomanonimizado",
    "dicomanonimizado": "mapeoiniciado",
    "mapeoiniciado": "parquetmapeado",
    "parquetmapeado": "procesamientoiniciado",
    "procesamientoiniciado": "datasetcreado",
}

# Eventos de fallo que requieren rollback
FALLOS_CRITICOS = {
    "mapeofallido": ["rollbackanonimacion"],
    "procesamientofallido": ["rollbackmapeo", "rollbackanonimacion"]
}

UUID_REGEX = re.compile(r"([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})")
EVENTO_LIMPIO_REGEX = re.compile(r"[^a-zA-Z]")  # Mantener solo letras para el tipo de evento

def configurar_logging():
    """ Configura los logs generales """
    fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_dir = "logs_saga"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"saga_{fecha_actual}.log")

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(log_file, mode="a"),
            logging.StreamHandler()
        ]
    )

def limpiar_evento(evento):
    """ 🧹 Limpieza de caracteres innecesarios y conversión a minúsculas """
    evento = evento.strip("*$.,& ")  # Elimina caracteres extraños
    evento = EVENTO_LIMPIO_REGEX.sub("", evento).lower()  # Mantiene solo letras
    return evento.lstrip("h")  # Elimina cualquier `h` residual

def extraer_id_y_evento(evento):
    """ Extrae el ID de saga y el tipo de evento de la cadena recibida """
    match = UUID_REGEX.search(evento)
    if match:
        saga_id = match.group(0)
        tipo_evento = evento.replace(saga_id, "").strip()
    else:
        saga_id = None
        tipo_evento = evento.strip()

    tipo_evento = limpiar_evento(tipo_evento)  # Normalizar el nombre del evento
    return saga_id, tipo_evento

def enviar_comando_rollback(comandos):
    """ Simulación del envío de comandos de rollback """
    for comando in comandos:
        logging.warning(f"🚨 Enviando comando de rollback: {comando}")

def main():
    global saga_id_global, estado_actual_global

    configurar_logging()
    logging.info("El coordinador de sagas ha iniciado.")
    
    broker_host = os.getenv('PULSAR_ADDRESS', default="broker")
    logging.info(f"Intentando conectar a Pulsar en pulsar://{broker_host}:6650...")

    try:
        client = pulsar.Client(f'pulsar://{broker_host}:6650')
        consumer = client.subscribe('eventos-saga', subscription_name='sagas_sub')
        logging.info("📡 Conectado a Pulsar y suscrito a `eventos-saga`.")
    except Exception as e:
        logging.error(f"❌ Error conectando a Pulsar: {e}")
        return

    logging.info("🔄 Esperando eventos...")
    try:
        while True:
            try:
                msg = consumer.receive(timeout_millis=5000)
                evento = msg.data().decode('utf-8')

                saga_id, tipo_evento = extraer_id_y_evento(evento)

                if not saga_id or not tipo_evento:
                    logging.warning(f"⚠️ Evento malformado recibido: {evento}")
                    continue

                consumer.acknowledge(msg)

                logging.info(f"📥 Recibido evento: {saga_id} {tipo_evento}")

                # 🟢 Iniciar una nueva saga si es `AnonimacionIniciada`
                if tipo_evento == "anonimacioniniciada":
                    saga_id_global = saga_id  # Guardamos el ID de saga
                    estado_actual_global = "anonimacioniniciada"
                    logging.info(f"🔥 Nueva saga iniciada con ID: {saga_id_global}")
                    continue

                # 🔴 Validar que haya una saga activa
                if saga_id_global is None:
                    logging.warning(f"⚠️ Evento {tipo_evento} recibido pero no hay una saga activa.")
                    continue

                # 🟠 Detectar eventos de fallo y enviar rollback
                if tipo_evento in FALLOS_CRITICOS:
                    logging.error(f"🚨 Fallo detectado en {tipo_evento}, enviando comandos de rollback.")
                    enviar_comando_rollback(FALLOS_CRITICOS[tipo_evento])
                    continue  # No seguir procesando esta saga

                # 🟠 Verificar si es el siguiente evento esperado
                if estado_actual_global in FLUJO_ESPERADO:
                    siguiente_esperado = FLUJO_ESPERADO[estado_actual_global]

                    if tipo_evento == siguiente_esperado:  # ✔️ Comparación exacta
                        estado_actual_global = tipo_evento  # 🔄 Actualizar el estado de la saga
                        logging.info(f"✅ Evento procesado correctamente: {tipo_evento}")

                        # 🏁 Finalizar la saga cuando se reciba `DatasetCreado`
                        if tipo_evento == "datasetcreado":
                            logging.info(f"🎉 Saga {saga_id_global} terminada con éxito.")
                            logging.info(f"📝 Cerrando log de la saga {saga_id_global}...")

                            # 🔄 Reiniciar la saga para una nueva
                            saga_id_global = None
                            estado_actual_global = None
                            continue  # Esperar una nueva saga

            except pulsar.Timeout:
                logging.debug("⏳ No se recibieron eventos en los últimos 5 segundos, esperando...")

    except KeyboardInterrupt:
        logging.info("🔴 Coordinador de sagas detenido manualmente.")
    finally:
        client.close()

if __name__ == '__main__':
    main()
