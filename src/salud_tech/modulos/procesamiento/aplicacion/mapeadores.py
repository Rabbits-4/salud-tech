from salud_tech.seedwork.aplicacion.dto import Mapeador as AppMap
from salud_tech.seedwork.dominio.repositorios import Mapeador as RepMap

from salud_tech.modulos.procesamiento.dominio.entidades import DatasetMedico
from salud_tech.modulos.procesamiento.dominio.objetos_valor import Estado, RegistroDeDiagnostico, Metadata

from .dto import DatasetMedicoDto, MetadataDto

from datetime import datetime

class MappeadorDatasetMedicoDTOJson(AppMap):
    def externo_a_dto(self, externo: dict) -> DatasetMedicoDto:
        dataset_medico_dto = DatasetMedicoDto(
            packet_id=externo.get('packet_id'),
            entorno_clinico=externo.get('entorno_clinico'),
            metadata=MetadataDto(
                registro_de_diagnostico=externo.get('registro_de_diagnostico'),
                fecha_creacion=externo.get('fecha_creacion'),
                fecha_actualizacion=externo.get('fecha_actualizacion'),
                historial_paciente_id=externo.get('historial_paciente_id'),
                contexto_procesal=externo.get('contexto_procesal'),
                notas_clinicas=externo.get('notas_clinicas'),                
            ),
            data=externo.get('data')
        )

        return dataset_medico_dto

    def dto_a_externo(self, dto: DatasetMedicoDto) -> dict:
        return dto.__dict__

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