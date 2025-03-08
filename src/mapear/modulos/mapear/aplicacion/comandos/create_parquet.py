from mapear.seedwork.aplicacion.comandos import Comando
from datetime import datetime
from .base import CrearBaseHandler
from dataclasses import dataclass

from mapear.modulos.mapear.aplicacion.mapeadores import MapeadorParquet
from mapear.modulos.mapear.aplicacion.dto import ParquetDto

from mapear.modulos.mapear.dominio.entidades import ParquetFile
from mapear.seedwork.infraestructura.uow import UnidadTrabajoPuerto

from mapear.seedwork.aplicacion.comandos import ejecutar_commando

from mapear.modulos.mapear.infraestructura.repositorios import RepositorioParquet

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

class CrearParquetHandler(CrearBaseHandler):

    def handle(self, comando: CreateParquet):
        parquet_dto = ParquetDto(
            packet_id=comando.packet_id,
            entorno_clinico=comando.entorno_clinico,
            registro_de_diagnostico=comando.registro_de_diagnostico,
            fecha_creacion=datetime.now(),
            fecha_actualizacion=datetime.now(),
            historial_paciente_id=comando.historial_paciente_id,
            contexto_procesal=comando.contexto_procesal,
            notas_clinicas=comando.notas_clinicas,
            data=comando.data
        )

        parquet: ParquetFile = self.fabrica_mapear.crear_objeto(parquet_dto, MapeadorParquet())
        parquet.crear_parquet(parquet)

        repositorio_parquet = self.fabrica_repositorio.crear_objeto(RepositorioParquet.__class__)

        UnidadTrabajoPuerto.registrar_batch(repositorio_parquet.agregar, parquet)
        UnidadTrabajoPuerto.savepoint() # que hace?
        UnidadTrabajoPuerto.commit()

@ejecutar_commando.register(CreateParquet)
def ejecutar_commando_create_parquet(comando: CreateParquet):
    handler = CrearParquetHandler()
    return handler.handle(comando)