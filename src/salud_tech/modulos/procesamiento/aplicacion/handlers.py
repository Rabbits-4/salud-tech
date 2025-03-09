from salud_tech.seedwork.aplicacion.handlers import Handler
from salud_tech.modulos.procesamiento.infraestructura.despachadores import Despachador
from salud_tech.modulos.procesamiento.aplicacion.comandos.create_dataset import CreateDatasetMedico
from salud_tech.seedwork.aplicacion.comandos import ejecutar_commando

import logging

class HandlerDatasetMedicoIntegracion(Handler):
    
    @staticmethod
    def handle_dataset_medico_creado(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-dataset-medico')

class HandlerEventoParquetCreado(Handler):
    """
    Maneja eventos de integración recibidos de Pulsar.
    """

    def handle(self, evento):
        logging.info(f"📡 [MAPEO] Procesando evento en el Handler")

        comando = CreateDatasetMedico(
            packet_id=evento["packet_id"],
            entorno_clinico=evento["entorno_clinico"],
            registro_de_diagnostico=evento["registro_de_diagnostico"],
            fecha_creacion=evento["fecha_creacion"],
            fecha_actualizacion=evento["fecha_actualizacion"],
            historial_paciente_id=evento["historial_paciente_id"],
            contexto_procesal=evento["contexto_procesal"],
            notas_clinicas=evento["notas_clinicas"],
            data=evento["data"]
        )

        logging.info("✅ [Procesamiento] Enviando comando `CreateDatasetMedico` para procesar los datos.")
        ejecutar_commando(comando)  # 🔹 Enviamos el comando para procesarlo