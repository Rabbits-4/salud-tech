from mapear.seedwork.aplicacion.dto import Mapeador as AppMap
from mapear.seedwork.dominio.repositorios import Mapeador as RepMap

from mapear.modulos.mapear.dominio.entidades import ParquetFile
from mapear.modulos.mapear.dominio.objetos_valor import Estado

from .dto import ParquetDto

class MappeadorParquetDTOJson(AppMap):
    def externo_a_dto(self, externo: dict) -> ParquetDto:
        dataset_medico_dto = ParquetDto(
            entorno_clinico=externo.get('entorno_clinico'),            
            fecha_creacion=externo.get('fecha_creacion'),
            fecha_actualizacion=externo.get('fecha_actualizacion'),
            registro_de_diagnostico=externo.get('registro_de_diagnostico'),
            historial_paciente_id=externo.get('token'),
            contexto_procesal=externo.get('contexto_procesal'),
            notas_clinicas=externo.get('notas_clinicas'),            
            data=externo.get('data')
        )

        return dataset_medico_dto

    def dto_a_externo(self, dto: ParquetDto) -> dict:
        return dto.__dict__

class MapeadorParquet(RepMap):

    def obtener_tipo(self) -> type:
        return ParquetFile.__class__
    
    def dto_a_entidad(self, dto: ParquetDto) -> ParquetFile:
        
        parquet = ParquetFile()
        parquet.fecha_creacion=dto.fecha_creacion
        parquet.fecha_actualizacion=dto.fecha_actualizacion
        parquet.contexto_procesal=dto.contexto_procesal
        parquet.historial_paciente_id=dto.historial_paciente_id
        parquet.registro_de_diagnostico=dto.registro_de_diagnostico
        parquet.notas_clinicas=dto.notas_clinicas
        parquet.data=dto.data
        parquet.estado=Estado.EN_PROCESO
        
        return parquet
    
    def entidad_a_dto(self, entidad: ParquetFile) -> ParquetDto:
        metadata_dto = ParquetDto(    
            entorno_clinico=entidad.entorno_clinico,        
            fecha_creacion=entidad.fecha_creacion,
            fecha_actualizacion=entidad.fecha_actualizacion,
            registro_de_diagnostico=entidad.registro_de_diagnostico,
            historial_paciente_id=entidad.historial_paciente_id,
            contexto_procesal=entidad.contexto_procesal,
            notas_clinicas=entidad.notas_clinicas,
            data=entidad.data,
        )

        return metadata_dto