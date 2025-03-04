from salud_tech.seedwork.aplicacion.servicios import Servicio
from salud_tech.modulos.procesamiento.dominio.entidades import DatasetMedico
from salud_tech.modulos.procesamiento.dominio.fabricas import FabricaProcesamiento
from salud_tech.modulos.procesamiento.infraestructura.fabricas import FabricaRepositorio
from salud_tech.modulos.procesamiento.infraestructura.repositorios import RepositorioParquet
from salud_tech.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from .mapeadores import MapeadorDatasetMedico

from .dto import ParquetDto

import asyncio

class ServicioDatasetMedico(Servicio):

    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_procesamiento: FabricaProcesamiento = FabricaProcesamiento()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_procesamiento(self):
        return self._fabrica_procesamiento       
    
    def crear_dataset_medico(self, dataset_dto: ParquetDto) -> ParquetDto:
        dataset: DatasetMedico = self.fabrica_procesamiento.crear_objeto(dataset_dto, MapeadorDatasetMedico())
        dataset.crear_dataset(dataset)

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioParquet.__class__)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, dataset)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()

        return self.fabrica_procesamiento.crear_objeto(dataset, MapeadorDatasetMedico())

    def obtener_dataset_medico_por_id(self, id) -> ParquetDto:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioParquet.__class__)
        return self.fabrica_procesamiento.crear_objeto(repositorio.obtener_por_id(id), MapeadorDatasetMedico())
