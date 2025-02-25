from salud_tech.seedwork.aplicacion.dto import Mapeador as AppMap
from salud_tech.seedwork.dominio.repositorios import Mapeador as RepMap

from salud_tech.modulos.procesamiento.dominio.entidades import DatasetMedico
from salud_tech.modulos.procesamiento.dominio.objetos_valor import Estado, RegistroDeDiagnostico, Metadata

from .dto import DatasetMedicoDto, MetadataDto

from datetime import datetime


class MapeadorDatasetMedico(RepMap):

    def obtener_tipo(self) -> type:
        return DatasetMedico
    
    def dto_a_entidad(self, dto: DatasetMedicoDto) -> DatasetMedico:
        dataset = DatasetMedico()
        dataset.registro_de_diagnostico = RegistroDeDiagnostico(
            region_anatomica=dto.metadata.registro_de_diagnostico,
            modalidad=dto.metadata.modalidad,
            patologia=dto.metadata.patologia
        )
        dataset.estado = Estado(dto.metadata.estado)
        return dataset
    
    def entidad_a_dto(self, entidad: DatasetMedico) -> DatasetMedicoDto:
        metadata_dto = MetadataDto(
            registro_de_diagnostico=entidad.registro_de_diagnostico.region_anatomica,
            fecha_creacion=entidad.fecha_creacion,
            fecha_actualizacion=entidad.fecha_actualizacion,
            historial_paciente_id=entidad.historial_paciente_id,
            contexto_procesal=entidad.contexto_procesal,
            notas_clinicas=entidad.notas_clinicas
        )
        return DatasetMedicoDto(
            packet_id=entidad.id,
            entorno_clinico=entidad.entorno_clinico,
            metadata=metadata_dto,
            data=entidad.data
        )