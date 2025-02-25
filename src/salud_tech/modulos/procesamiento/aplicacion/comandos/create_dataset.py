from salud_tech.seedwork.aplicacion.comandos import Comando, ComandoHandler
from datetime import datetime
from .base import CrearBaseHandler

from salud_tech.modulos.procesamiento.aplicacion.mapeadores import MapeadorDatasetMedico
from salud_tech.modulos.procesamiento.aplicacion.dto import MetadataDto, DatasetMedicoDto

from salud_tech.modulos.procesamiento.dominio.entidades import DatasetMedico
from salud_tech.seedwork.infraestructura.uow import UnidadTrabajoPuerto

from salud_tech.modulos.procesamiento.infraestructura.repositorios import RepositorioDatasetMedico

class CreateDataset(Comando):
    packet_id: str
    entorno_clinico: str
    metadata: MetadataDto
    data: any
    registro_de_diagnostico: dict
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    historial_paciente_id: str
    contexto_procesal: str
    notas_clinicas: str

class CreateDatasetHandler(CrearBaseHandler):

    def handle(self, comando: CreateDataset):
        dataset_dto = DatasetMedicoDto(
            packet_id=comando.packet_id,
            entorno_clinico=comando.entorno_clinico,
            metadata={
                "registro_de_diagnostico": comando.registro_de_diagnostico,
                "fecha_creacion": datetime.now(),
                "fecha_actualizacion": datetime.now(),
                "historial_paciente_id": comando.historial_paciente_id,
                "contexto_procesal": comando.contexto_procesal,
                "notas_clinicas": comando.notas_clinicas
            },
            data=comando.data
        )

        dataset: DatasetMedico = self.fabrica_procesamiento.crear_objeto(dataset_dto, MapeadorDatasetMedico())
        dataset.creat_dataset(dataset)

        dataset = self.fabrica_repositorio.crear_objeto(RepositorioDatasetMedico.__class__)

        UnidadTrabajoPuerto.registrar_batch(dataset.agregar_evento, dataset)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()
