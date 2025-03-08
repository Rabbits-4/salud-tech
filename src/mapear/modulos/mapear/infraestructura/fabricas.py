""" Fábricas para la creación de objetos en la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos en la capa de infraestructura del dominio de vuelos

"""

from dataclasses import dataclass
from mapear.seedwork.dominio.fabricas import Fabrica
from mapear.seedwork.dominio.repositorios import Repositorio

from mapear.modulos.mapear.dominio.repositorios import RepositorioParquet
from .repositorios import RepositorioParquetPostgress

from .excepciones import ExcepcionFabrica

@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        if obj == RepositorioParquet.__class__:
            return RepositorioParquetPostgress()
        else:
            raise ExcepcionFabrica()
