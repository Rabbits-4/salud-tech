""" Mapeadores para la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs

"""

from mapear.seedwork.dominio.repositorios import Mapeador
from mapear.modulos.procesamiento.dominio.objetos_valor import RegionAnatomica, Modalidad, Patologia, EntornoClinico, NotasClinicas, HistorialPaciente, ContextoProcesal, Imagen, Metadata, RegistroDeDiagnostico
from mapear.modulos.procesamiento.dominio.entidades import ParquetFile
from .dto import Parquet

class MapeadorParquet(Mapeador):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def obtener_tipo(self) -> type:
        return ParquetFile.__class__

    def entidad_a_dto(self, entidad: ParquetFile) -> Parquet:
        id = str(entidad.id)
        registro_de_diagnostico = entidad.registro_de_diagnostico
        contextos_procesales = entidad.contexto_procesal
        notas_clinicas = entidad.notas_clinicas
        data = entidad.data
        estado = entidad.estado


        parquet_dto = Parquet(
            id=id,
            registro_de_diagnostico=registro_de_diagnostico,
            contextos_procesales=contextos_procesales,
            notas_clinicas=notas_clinicas,
            data=data,
            estado = "En Proceso"
        )

        return parquet_dto

    def dto_a_entidad(self, dto: Parquet) -> ParquetFile:
        parquet = ParquetFile(
            id=dto.id,
            registro_de_diagnostico=dto.registro_de_diagnostico,
            contextos_procesales=dto.contextos_procesales,
            notas_clinicas=dto.notas_clinicas,
            data=dto.data,
            estado=dto.estado
        )        
        
        return parquet