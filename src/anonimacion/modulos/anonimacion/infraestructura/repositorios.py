""" Repositorios para el manejo de persistencia de objetos de dominio en la capa de infraestructura del dominio de anonimación.

En este archivo usted encontrará los diferentes repositorios para
persistir objetos dominio (agregaciones) en la capa de infraestructura del dominio de anonimación.
"""

from anonimacion.modulos.anonimacion.dominio.fabricas import FabricaAnonimacion
from anonimacion.modulos.anonimacion.dominio.entidades import DicomAnonimo
from anonimacion.modulos.anonimacion.dominio.repositorios import RepositorioDicomAnonimo
from .dto import DicomAnonimo as DicomAnonimoDTO
from .mapeadores import MapeadorDicomAnonimo
from anonimacion.config.db import db
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
        db.session.add(dto)
        db.session.commit()

    def actualizar(self, dicom_anonimo: DicomAnonimo):
        """
        Actualiza un registro en la base de datos.
        """
        dto = DicomAnonimoDTO.query.filter_by(id=dicom_anonimo.id).first()
        if dto:
            dto.imagen = dicom_anonimo.imagen
            dto.entorno_clinico = dicom_anonimo.entorno_clinico
            dto.registro_de_diagnostico = dicom_anonimo.registro_de_diagnostico
            dto.fecha_actualizacion = dicom_anonimo.fecha_actualizacion
            dto.contexto_procesal = dicom_anonimo.contexto_procesal
            dto.notas_clinicas = dicom_anonimo.notas_clinicas
            dto.data = dicom_anonimo.data
            db.session.commit()

    def eliminar(self, id: UUID):
        """
        Elimina un registro de la base de datos.
        """
        dto = DicomAnonimoDTO.query.filter_by(id=str(id)).first()
        if dto:
            db.session.delete(dto)
            db.session.commit()

    def obtener_todos(self):
        """
        Obtiene todos los registros de la base de datos.
        """
        dtos = DicomAnonimoDTO.query.all()
        return [MapeadorDicomAnonimo().dto_a_entidad(dto) for dto in dtos]
