from salud_tech.seedwork.aplicacion.comandos import Comando
from datetime import datetime
from .base import CrearBaseHandler
from dataclasses import dataclass, field

from salud_tech.modulos.procesamiento.aplicacion.mapeadores import MapeadorDatasetMedico
from salud_tech.modulos.procesamiento.aplicacion.dto import MetadataDto, ParquetDto

from salud_tech.modulos.procesamiento.dominio.entidades import DatasetMedico
from salud_tech.seedwork.infraestructura.uow import UnidadTrabajoPuerto

from salud_tech.seedwork.aplicacion.comandos import ejecutar_commando

from salud_tech.modulos.procesamiento.infraestructura.repositorios import RepositorioParquet

@dataclass
class CreateParquet(Comando):
    packet_id: str
    entorno_clinico: str
    registro_de_diagnostico: dict
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    historial_paciente_id: str
    contexto_procesal: str
    notas_clinicas: str
    data: any

class CreateParquetHandler(CrearBaseHandler):

    def handle(self, comando: CreateParquet):
        metadata_dto = MetadataDto(
            registro_de_diagnostico=comando.registro_de_diagnostico,
            fecha_creacion=datetime.now(),
            fecha_actualizacion=datetime.now(),
            historial_paciente_id=comando.historial_paciente_id,
            contexto_procesal=comando.contexto_procesal,
            notas_clinicas=comando.notas_clinicas
        )

        dataset_dto = ParquetDto(
            packet_id=comando.packet_id,
            entorno_clinico=comando.entorno_clinico,
            metadata=metadata_dto,
            data=comando.data
        )

        dataset: DatasetMedico = self.fabrica_procesamiento.crear_objeto(dataset_dto, MapeadorDatasetMedico())
        dataset.crear_dataset(dataset)

        repositorio_dataset = self.fabrica_repositorio.crear_objeto(RepositorioParquet.__class__)

        UnidadTrabajoPuerto.registrar_batch(repositorio_dataset.agregar, dataset)
        UnidadTrabajoPuerto.savepoint() # que hace?
        UnidadTrabajoPuerto.commit()

@ejecutar_commando.register(CreateParquet)
def ejecutar_commando_create_dataset_medico(comando: CreateParquet):
    handler = CreateParquetHandler()
    return handler.handle(comando)