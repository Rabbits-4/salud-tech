""" Mapeadores para la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs

"""

from mapear.seedwork.dominio.repositorios import Mapeador
from mapear.modulos.mapear.dominio.entidades import ParquetFile
from .dto import Parquet

class MapeadorParquet(Mapeador):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def obtener_tipo(self) -> type:
        return ParquetFile.__class__

    def entidad_a_dto(self, entidad: ParquetFile) -> Parquet:
        id = str(entidad.id)
        registro_de_diagnostico = entidad.registro_de_diagnostico
        contexto_procesal = entidad.contexto_procesal
        notas_clinicas = entidad.notas_clinicas
        data = entidad.data

        parquet_dto = Parquet(
            registro_de_diagnostico=registro_de_diagnostico,
            contexto_procesal=contexto_procesal,
            notas_clinicas=notas_clinicas,
            data=data,
            estado = "En Proceso"
        )

        return parquet_dto

    def dto_a_entidad(self, dto: Parquet) -> ParquetFile:
        parquet = ParquetFile(
            id=dto.id,
            packet_id=dto.id,
            fecha_creacion=dto.fecha_creacion,
            fecha_actualizacion=dto.fecha_actualizacion,
            registro_de_diagnostico=dto.registro_de_diagnostico,
            contexto_procesal=dto.contexto_procesal,
            notas_clinicas=dto.notas_clinicas,
            data=dto.data,
            estado=dto.estado
        )        
        
        return parquet