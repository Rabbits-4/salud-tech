""" Fábricas para la creación de objetos en la capa de infraestructura del dominio de anonimación

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos en la capa de infraestructura del dominio de anonimación.

"""

from dataclasses import dataclass
from anonimacion.seedwork.dominio.fabricas import Fabrica
from anonimacion.seedwork.dominio.repositorios import Repositorio

from anonimacion.modulos.anonimacion.dominio.repositorios import RepositorioDicomAnonimo
from .repositorios import RepositorioDicomAnonimoPostgres

from .excepciones import ExcepcionFabrica

@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        if obj == RepositorioDicomAnonimo.__class__:
            return RepositorioDicomAnonimoPostgres()
        else:
            raise ExcepcionFabrica()