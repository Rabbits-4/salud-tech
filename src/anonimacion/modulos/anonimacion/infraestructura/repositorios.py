""" Repositorios para el manejo de persistencia de objetos de dominio en la capa de infraestructura del dominio de anonimación.

En este archivo usted encontrará los diferentes repositorios para
persistir objetos dominio (agregaciones) en la capa de infraestructura del dominio de anonimación.
"""

from anonimacion.modulos.anonimacion.dominio.fabricas import FabricaAnonimacion
from anonimacion.modulos.anonimacion.dominio.entidades import DicomAnonimo
from anonimacion.modulos.anonimacion.dominio.repositorios import RepositorioDicomAnonimo

from .dto import DicomAnonimo as DicomAnonimoDTO
from .mapeadores import MapeadorDicomAnonimo
from uuid import UUID
import logging

class RepositorioDicomAnonimoPostgres(RepositorioDicomAnonimo):

    def __init__(self):
        self._fabrica_anonimacion: FabricaAnonimacion = FabricaAnonimacion()

    @property
    def fabrica_anonimacion(self):
        return self._fabrica_anonimacion

    def obtener_por_id(self, id: UUID) -> DicomAnonimo:
        dto = DicomAnonimoDTO.query.filter_by(id=str(id)).first()
        if dto:
            return MapeadorDicomAnonimo().dto_a_entidad(dto)
        return None

    def agregar(self, dicom_anonimo: DicomAnonimo):
        dto = MapeadorDicomAnonimo().entidad_a_dto(dicom_anonimo)
        from anonimacion.config.db import db
        db.session.add(dto)
        db.session.commit()

    def eliminar_por_id(self, id: UUID):
        from anonimacion.config.db import db
        dto = DicomAnonimoDTO.query.filter_by(id=str(id)).first()
        if dto:
            db.session.delete(dto)
            db.session.commit()