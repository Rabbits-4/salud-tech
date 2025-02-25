""" Repositorios para el manejo de persistencia de objetos de dominio en la capa de infraestructura del dominio de procesamiento de datos médicos

En este archivo usted encontrará los diferentes repositorios para
persistir objetos dominio (agregaciones) en la capa de infraestructura del dominio de procesamiento de datos médicos

"""

from salud_tech.config.db import db
from salud_tech.modulos.procesamiento.dominio.repositorios import RepositorioDatasetMedico
from salud_tech.modulos.procesamiento.dominio.fabricas import FabricaProcesamiento
from salud_tech.modulos.procesamiento.dominio.entidades import DatasetMedico
from salud_tech.modulos.procesamiento.dominio.objetos_valor import Estado, RegistroDeDiagnostico, Metadata
from .dto import DatasetMedicoDTO
from .mapeadores import MapeadorDatasetMedico
from uuid import UUID

class RepositorioDatasetMedicoPostgres(RepositorioDatasetMedico):

    def __init__(self):
        self._fabrica_procesamiento: FabricaProcesamiento = FabricaProcesamiento()

    @property
    def fabrica_procesamiento(self):
        return self._fabrica_procesamiento

    def obtener_por_id(self, id: UUID) -> DatasetMedico:
        dataset_medico_dto = db.session.query(DatasetMedicoDTO).filter_by(id=str(id)).one()
        return self.fabrica_procesamiento.crear_objeto(dataset_medico_dto, MapeadorDatasetMedico())

    def obtener_todos(self) -> list[DatasetMedico]:
        return [self.fabrica_procesamiento.crear_objeto(dto, MapeadorDatasetMedico()) for dto in db.session.query(DatasetMedicoDTO).all()]

    def agregar(self, dataset: DatasetMedico):
        dataset_dto = self.fabrica_procesamiento.crear_objeto(dataset, MapeadorDatasetMedico())
        db.session.add(dataset_dto)

    def actualizar(self, dataset: DatasetMedico):
        dataset_dto = self.fabrica_procesamiento.crear_objeto(dataset, MapeadorDatasetMedico())
        db.session.merge(dataset_dto)

    def eliminar(self, dataset_id: UUID):
        db.session.query(DatasetMedicoDTO).filter_by(id=str(dataset_id)).delete()
