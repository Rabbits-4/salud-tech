""" Mapeadores para la capa de infraestructura del dominio de anonimación

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs.

"""
from anonimacion.seedwork.dominio.repositorios import Mapeador
from anonimacion.modulos.anonimacion.dominio.objetos_valor import RegistroDeDiagnostico
from anonimacion.modulos.anonimacion.dominio.entidades import DicomAnonimo
from .dto import DicomAnonimo as DicomAnonimoDTO

import logging

class MapeadorDicomAnonimo(Mapeador):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def obtener_tipo(self) -> type:
        return DicomAnonimo.__class__

    def entidad_a_dto(self, entidad: DicomAnonimo) -> DicomAnonimoDTO:
        return DicomAnonimoDTO(
            id=str(entidad.id),
            imagen=entidad.imagen,
            entorno_clinico=entidad.entorno_clinico,
            registro_de_diagnostico=entidad.registro_de_diagnostico,
            fecha_creacion=entidad.fecha_creacion,
            fecha_actualizacion=entidad.fecha_actualizacion,
            contexto_procesal=entidad.contexto_procesal,
            notas_clinicas=entidad.notas_clinicas,
            data=entidad.data
        )

    def dto_a_entidad(self, dto: DicomAnonimoDTO) -> DicomAnonimo:
        return DicomAnonimo(
            id=dto.id,
            imagen=dto.imagen,
            entorno_clinico=dto.entorno_clinico,
            registro_de_diagnostico=dto.registro_de_diagnostico,
            fecha_creacion=dto.fecha_creacion,
            fecha_actualizacion=dto.fecha_actualizacion,
            contexto_procesal=dto.contexto_procesal,
            notas_clinicas=dto.notas_clinicas,
            data=dto.data
        )