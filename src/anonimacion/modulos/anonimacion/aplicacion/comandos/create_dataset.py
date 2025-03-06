from anonimacion.seedwork.aplicacion.comandos import Comando
from datetime import datetime
from .base import CrearBaseHandler
from dataclasses import dataclass, field

from anonimacion.modulos.anonimacion.aplicacion.mapeadores import MapeadorDatasetMedico
from anonimacion.modulos.anonimacion.aplicacion.dto import MetadataDto, DatasetMedicoDto

from anonimacion.modulos.anonimacion.dominio.entidades import DatasetMedico
from anonimacion.seedwork.infraestructura.uow import UnidadTrabajoPuerto

from anonimacion.seedwork.aplicacion.comandos import ejecutar_commando

from anonimacion.modulos.anonimacion.infraestructura.repositorios import RepositorioDatasetMedico

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

        UnidadTrabajoPuerto.registrar_batch(repositorio_dataset.agregar, dataset)
        UnidadTrabajoPuerto.savepoint() # que hace?
        UnidadTrabajoPuerto.commit()

@ejecutar_commando.register(CreateDatasetMedico)
def ejecutar_commando_create_dataset_medico(comando: CreateDatasetMedico):
    handler = CreateDatasetHandler()
    return handler.handle(comando)