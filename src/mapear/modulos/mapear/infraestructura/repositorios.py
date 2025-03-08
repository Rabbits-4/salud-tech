""" Repositorios para el manejo de persistencia de objetos de dominio en la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará las diferentes repositorios para
persistir objetos dominio (agregaciones) en la capa de infraestructura del dominio de vuelos

"""

# from mapear.config.db import db

from mapear.modulos.mapear.dominio.fabricas import FabricaMapear
from mapear.modulos.mapear.dominio.entidades import ParquetFile
from mapear.modulos.mapear.dominio.repositorios import RepositorioParquet

from .dto import Parquet as Parquet
from .mapeadores import MapeadorParquet
from uuid import UUID

class RepositorioParquetPostgress(RepositorioParquet):

    def __init__(self):
        self._fabrica_parquet: FabricaMapear = FabricaMapear()

    @property
    def fabrica_parquet(self):
        return self._fabrica_parquet

    def obtener_por_id(self, id: UUID) -> ParquetFile:
        from mapear.config.db import db
        parquet_dto = db.session.query(Parquet).filter_by(id=str(id)).one()
        return self.fabrica_parquet.crear_objeto(parquet_dto, MapeadorParquet())

    def obtener_todos(self) -> list[ParquetFile]:
        # TODO
        raise NotImplementedError

    def agregar(self, parquet: ParquetFile):
        from mapear.config.db import db
        parquet_dto = self.fabrica_parquet.crear_objeto(parquet, MapeadorParquet())
        db.session.add(parquet_dto)
        db.session.commit()

    def actualizar(self, parquet: ParquetFile):
        # TODO
        raise NotImplementedError

    def eliminar(self, parquet_id: UUID):
        # TODO
        raise NotImplementedError