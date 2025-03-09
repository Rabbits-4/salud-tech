from mapear.seedwork.aplicacion.handlers import Handler
from mapear.modulos.mapear.infraestructura.despachadores import Despachador
from mapear.modulos.mapear.aplicacion.comandos.create_parquet import CreateParquet
from mapear.seedwork.aplicacion.comandos import ejecutar_commando

import logging

class HandlerParquetIntegracion(Handler):
    
    @staticmethod
    def handle_parquet_creado(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'mapear.parquet.creado')

class HandlerEventoDicomAnonimizado(Handler):
    """
    Maneja eventos de integración recibidos de Pulsar.
    """

    def handle(self, evento):
        logging.info(f"📡 [MAPEO] Procesando evento en el Handler: {evento}")

        comando = CreateParquet(
            entorno_clinico=evento["entorno_clinico"],
            registro_de_diagnostico=evento["registro_de_diagnostico"],
            fecha_creacion=evento["fecha_creacion"],
            fecha_actualizacion=evento["fecha_actualizacion"],
            historial_paciente_id=evento["id_dicom_anonimo"],
            contexto_procesal=evento["contexto_procesal"],
            notas_clinicas=evento["notas_clinicas"],
            data=evento["data"]
        )

        logging.info("✅ [MAPEO] Enviando comando `CreateParquet` para procesar los datos.")
        ejecutar_commando(comando)  # 🔹 Enviamos el comando para procesarlo