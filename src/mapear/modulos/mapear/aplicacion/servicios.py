from mapear.seedwork.aplicacion.servicios import Servicio
from mapear.modulos.mapear.dominio.entidades import ParquetFile
from mapear.modulos.mapear.dominio.fabricas import FabricaMapear
from mapear.modulos.mapear.infraestructura.fabricas import FabricaRepositorio
from mapear.modulos.mapear.infraestructura.repositorios import RepositorioParquet
from mapear.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from .mapeadores import MapeadorParquet

from .dto import ParquetDto

import asyncio

class ServicioParquet(Servicio):

    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_procesamiento: FabricaMapear = FabricaMapear()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_procesamiento(self):
        return self._fabrica_procesamiento       
    
    def crear_parquet_medico(self, dataset_dto: ParquetDto) -> ParquetDto:
        parquet: ParquetFile = self.fabrica_procesamiento.crear_objeto(dataset_dto, MapeadorParquet())
        parquet.crear_parquet(parquet)

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioParquet.__class__)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, parquet)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()

        return self.fabrica_procesamiento.crear_objeto(parquet, MapeadorParquet())

    def obtener_parquet_por_id(self, id) -> ParquetDto:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioParquet.__class__)
        return self.fabrica_procesamiento.crear_objeto(repositorio.obtener_por_id(id), MapeadorParquet())
