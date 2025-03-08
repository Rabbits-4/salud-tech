""" Fábricas para la creación de objetos del dominio de procesamiento de datos médicos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos del dominio de procesamiento de datos médicos

"""

from .entidades import ParquetFile
from .excepciones import TipoObjetoNoExisteEnDominioProcesamientoExcepcion
from mapear.seedwork.dominio.repositorios import Mapeador, Repositorio
from mapear.seedwork.dominio.fabricas import Fabrica
from mapear.seedwork.dominio.entidades import Entidad
from dataclasses import dataclass

@dataclass
class _FabricaParquet(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad):
            return mapeador.entidad_a_dto(obj)
        else:
            parquet: ParquetFile = mapeador.dto_a_entidad(obj)
            return parquet

@dataclass
class FabricaMapear(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == ParquetFile.__class__:
            fabrica_parquet = _FabricaParquet()
            return fabrica_parquet.crear_objeto(obj, mapeador)
        else:
            raise TipoObjetoNoExisteEnDominioProcesamientoExcepcion()
