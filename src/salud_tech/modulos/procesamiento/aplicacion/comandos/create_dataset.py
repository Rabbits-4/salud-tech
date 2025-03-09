from salud_tech.seedwork.aplicacion.comandos import Comando
from datetime import datetime
from .base import CrearBaseHandler
from dataclasses import dataclass, field
import json
import logging

from salud_tech.modulos.procesamiento.aplicacion.mapeadores import MapeadorDatasetMedico
from salud_tech.modulos.procesamiento.aplicacion.dto import MetadataDto, DatasetMedicoDto
from salud_tech.modulos.procesamiento.dominio.entidades import DatasetMedico
from salud_tech.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from salud_tech.seedwork.aplicacion.comandos import ejecutar_commando
from salud_tech.modulos.procesamiento.infraestructura.repositorios import RepositorioDatasetMedico



@dataclass
class CreateDatasetMedico(Comando):
    packet_id: str
    entorno_clinico: str
    registro_de_diagnostico: dict
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    historial_paciente_id: str
    contexto_procesal: str
    notas_clinicas: str
    data: any

class CreateDatasetHandler(CrearBaseHandler):

    def handle(self, comando: CreateDatasetMedico):
        logging.info("🚀 [Procesamiento] Iniciando proceso de creación de Dataset...")

        metadata_dto = MetadataDto(
            registro_de_diagnostico=comando.registro_de_diagnostico,
            fecha_creacion=datetime.now(),
            fecha_actualizacion=datetime.now(),
            historial_paciente_id=comando.historial_paciente_id,
            contexto_procesal=comando.contexto_procesal,
            notas_clinicas=comando.notas_clinicas
        )

        dataset_dto = DatasetMedicoDto(
            packet_id=comando.packet_id,
            entorno_clinico=comando.entorno_clinico,
            metadata=metadata_dto,
            data=comando.data
        )

        dataset: DatasetMedico = self.fabrica_procesamiento.crear_objeto(dataset_dto, MapeadorDatasetMedico())
        dataset.crear_dataset(dataset)

        repositorio_dataset = self.fabrica_repositorio.crear_objeto(RepositorioDatasetMedico.__class__)
        
        from salud_tech.config.uow import UnidadTrabajoSQLAlchemy
        from salud_tech.config.db import db
        from salud_tech.api import create_app

        app = create_app({"TESTINT": True})  # 🔹 Creamos la instancia de Flask para contexto

        with app.app_context():
            try:
                with UnidadTrabajoSQLAlchemy() as uow:
                    repositorio_dataset.agregar(dataset)
                    uow.commit()
                    logging.info(f"✅ [Procesamiento] Dataset `{dataset.id}` guardado exitosamente.")
                
            except Exception as e:
                logging.error(f"❌ [Procesamiento] Error guardando Dataset en BD: {e}")
                raise e
            finally:
                db.session.close()
                logging.info("🚀 db session cerrada exitosamente")
                
@ejecutar_commando.register(CreateDatasetMedico)
def ejecutar_commando_create_dataset_medico(comando: CreateDatasetMedico):
    handler = CreateDatasetHandler()
    return handler.handle(comando)