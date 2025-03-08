from mapear.seedwork.aplicacion.dto import Mapeador as AppMap
from mapear.seedwork.dominio.repositorios import Mapeador as RepMap

from mapear.modulos.procesamiento.dominio.entidades import ParquetFile
from mapear.modulos.procesamiento.dominio.objetos_valor import Estado, RegistroDeDiagnostico, Metadata

from .dto import ParquetDto, MetadataDto

class MappeadorParquetDTOJson(AppMap):
    def externo_a_dto(self, externo: dict) -> ParquetDto:
        dataset_medico_dto = ParquetDto(
            packet_id=externo.get('packet_id'),
            entorno_clinico=externo.get('entorno_clinico'),            
            registro_de_diagnostico=externo.get('registro_de_diagnostico'),
            fecha_creacion=externo.get('fecha_creacion'),
            fecha_actualizacion=externo.get('fecha_actualizacion'),
            historial_paciente_id=externo.get('historial_paciente_id'),
            contexto_procesal=externo.get('contexto_procesal'),
            notas_clinicas=externo.get('notas_clinicas'),            
            data=externo.get('data')
        )

        return dataset_medico_dto

    def dto_a_externo(self, dto: ParquetDto) -> dict:
        return dto.__dict__

class MapeadorParquet(RepMap):

    def obtener_tipo(self) -> type:
        return DatasetMedico.__class__
    
    def dto_a_entidad(self, dto: ParquetDto) -> DatasetMedico:
        registro_dict = dto.metadata.registro_de_diagnostico  
        dataset = DatasetMedico()
        dataset.registro_de_diagnostico = RegistroDeDiagnostico(
            region_anatomica=registro_dict.get('region_anatomica'),
            modalidad=registro_dict.get('modalidad'),
            patologia=registro_dict.get('patologia')
        )

        estado_valor = dto.metadata.estado if hasattr(dto.metadata, 'estado') and dto.metadata.estado else "Pendiente"
        dataset.estado = Estado(estado_valor)
        return dataset
    
    def entidad_a_dto(self, entidad: DatasetMedico) -> ParquetDto:
        metadata_dto = MetadataDto(
            registro_de_diagnostico=entidad.registro_de_diagnostico.region_anatomica,
            fecha_creacion=entidad.fecha_creacion,
            fecha_actualizacion=entidad.fecha_actualizacion,
            historial_paciente_id=entidad.historial_paciente_id,
            contexto_procesal=entidad.contexto_procesal,
            notas_clinicas=entidad.notas_clinicas
        )
        return ParquetDto(
            packet_id=entidad.id,
            entorno_clinico=entidad.entorno_clinico,
            metadata=metadata_dto,
            data=entidad.data
        )