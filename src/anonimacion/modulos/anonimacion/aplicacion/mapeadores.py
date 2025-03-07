from anonimacion.seedwork.aplicacion.dto import Mapeador as AppMap
from anonimacion.seedwork.dominio.repositorios import Mapeador as RepMap

from anonimacion.modulos.anonimacion.dominio.entidades import DicomAnonimo
from anonimacion.modulos.anonimacion.dominio.objetos_valor import RegistroDeDiagnostico

from .dto import DicomAnonimoDto
import logging

from datetime import datetime

class MapeadorDicomAnonimoDTOJson(AppMap):
    def externo_a_dto(self, externo: dict) -> DicomAnonimoDto:
        return DicomAnonimoDto(
            packet_id=externo.get('packet_id', ''),
            imagen=externo.get('imagen', ''),
            entorno_clinico=externo.get('entorno_clinico', ''),
            registro_de_diagnostico=externo.get('registro_de_diagnostico', {}),
            fecha_creacion=datetime.fromisoformat(externo.get('fecha_creacion', datetime.utcnow().isoformat())),
            fecha_actualizacion=datetime.fromisoformat(externo.get('fecha_actualizacion', datetime.utcnow().isoformat())),
            contexto_procesal=externo.get('contexto_procesal', ''),
            notas_clinicas=externo.get('notas_clinicas', ''),
            data=externo.get('data', {})
        )

    def dto_a_externo(self, dto: DicomAnonimoDto) -> dict:
        return {
            'packet_id': dto.packet_id,
            'imagen': dto.imagen,
            'entorno_clinico': dto.entorno_clinico,
            'registro_de_diagnostico': dto.registro_de_diagnostico,
            'fecha_creacion': dto.fecha_creacion.isoformat(),
            'fecha_actualizacion': dto.fecha_actualizacion.isoformat(),
            'contexto_procesal': dto.contexto_procesal,
            'notas_clinicas': dto.notas_clinicas,
            'data': dto.data
        }

    def dto_a_entidad(self, dto: DicomAnonimoDto) -> DicomAnonimo:
        return DicomAnonimo(
            id=dto.packet_id,
            imagen=dto.imagen,
            entorno_clinico=dto.entorno_clinico,
            registro_de_diagnostico=dto.registro_de_diagnostico,
            fecha_creacion=dto.fecha_creacion.isoformat(),
            fecha_actualizacion=dto.fecha_actualizacion.isoformat(),
            contexto_procesal=dto.contexto_procesal,
            notas_clinicas=dto.notas_clinicas,
            data=dto.data
        )

    def entidad_a_dto(self, entidad: DicomAnonimo) -> DicomAnonimoDto:
        return DicomAnonimoDto(
            packet_id=entidad.id,
            imagen=entidad.imagen,
            entorno_clinico=entidad.entorno_clinico,
            registro_de_diagnostico=entidad.registro_de_diagnostico,
            fecha_creacion=datetime.fromisoformat(entidad.fecha_creacion),
            fecha_actualizacion=datetime.fromisoformat(entidad.fecha_actualizacion),
            contexto_procesal=entidad.contexto_procesal,
            notas_clinicas=entidad.notas_clinicas,
            data=entidad.data
        )