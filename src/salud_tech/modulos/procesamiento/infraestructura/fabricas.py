""" Fábricas para la creación de objetos en la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos en la capa de infraestructura del dominio de vuelos

"""

from dataclasses import dataclass
from salud_tech.seedwork.dominio.fabricas import Fabrica
from salud_tech.seedwork.dominio.repositorios import Repositorio

from salud_tech.modulos.procesamiento.dominio.repositorios import RepositorioDatasetMedico
from .repositorios import RepositorioDatasetMedicoPostgress

from .excepciones import ExcepcionFabrica

@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        if obj == RepositorioDatasetMedico.__class__:
            return RepositorioDatasetMedicoPostgress()
        else:
            raise ExcepcionFabrica()
