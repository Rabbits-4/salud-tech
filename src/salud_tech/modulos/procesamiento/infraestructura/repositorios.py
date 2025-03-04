""" Repositorios para el manejo de persistencia de objetos de dominio en la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará las diferentes repositorios para
persistir objetos dominio (agregaciones) en la capa de infraestructura del dominio de vuelos

"""

# from salud_tech.config.db import db

from salud_tech.modulos.procesamiento.dominio.fabricas import FabricaProcesamiento
from salud_tech.modulos.procesamiento.dominio.entidades import DatasetMedico
from salud_tech.modulos.procesamiento.dominio.repositorios import RepositorioDatasetMedico

from .dto import DatasetMedico as DatasetMedicoDTO
from .mapeadores import MapeadorDatasetMedico
from uuid import UUID

class RepositorioDatasetMedicoPostgress(RepositorioDatasetMedico):

    def __init__(self):
        self._fabrica_procesamiento: FabricaProcesamiento = FabricaProcesamiento()

    @property
    def fabrica_procesamiento(self):
        return self._fabrica_procesamiento

    def obtener_por_id(self, id: UUID) -> DatasetMedico:
        dataset_medico_dto = db.session.query(DatasetMedicoDTO).filter_by(id=str(id)).one()
        return self.fabrica_procesamiento.crear_objeto(dataset_medico_dto, MapeadorDatasetMedico())

    def obtener_todos(self) -> list[DatasetMedico]:
        # TODO
        raise NotImplementedError

    def agregar(self, dataset_medico: DatasetMedico):
        from salud_tech.config.db import db
        dataset_medico_dto = self.fabrica_procesamiento.crear_objeto(dataset_medico, MapeadorDatasetMedico())
        db.session.add(dataset_medico_dto)

    def actualizar(self, dataset_medico: DatasetMedico):
        # TODO
        raise NotImplementedError

    def eliminar(self, dataset_medico_id: UUID):
        # TODO
        raise NotImplementedError