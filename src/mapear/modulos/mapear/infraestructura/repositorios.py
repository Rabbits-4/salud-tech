""" Repositorios para el manejo de persistencia de objetos de dominio en la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará las diferentes repositorios para
persistir objetos dominio (agregaciones) en la capa de infraestructura del dominio de vuelos

"""

# from mapear.config.db import db

from mapear.modulos.mapear.dominio.fabricas import FabricaProcesamiento
from mapear.modulos.mapear.dominio.entidades import ParquetFile
from mapear.modulos.mapear.dominio.repositorios import RepositorioParquet

from .dto import Parquet as Parquet
from .mapeadores import MapeadorParquet
from uuid import UUID

class RepositorioParquetPostgress(RepositorioParquet):

    def __init__(self):
        self._fabrica_procesamiento: FabricaProcesamiento = FabricaProcesamiento()

    @property
    def fabrica_procesamiento(self):
        return self._fabrica_procesamiento

    def obtener_por_id(self, id: UUID) -> ParquetFile:
        from mapear.config.db import db
        dataset_medico_dto = db.session.query(Parquet).filter_by(id=str(id)).one()
        return self.fabrica_procesamiento.crear_objeto(dataset_medico_dto, MapeadorParquet())

    def obtener_todos(self) -> list[ParquetFile]:
        # TODO
        raise NotImplementedError

    def agregar(self, dataset_medico: ParquetFile):
        from mapear.config.db import db
        dataset_medico_dto = self.fabrica_procesamiento.crear_objeto(dataset_medico, MapeadorParquet())
        db.session.add(dataset_medico_dto)

    def actualizar(self, dataset_medico: ParquetFile):
        # TODO
        raise NotImplementedError

    def eliminar(self, dataset_medico_id: UUID):
        # TODO
        raise NotImplementedError