""" Fábricas para la creación de objetos en la capa de infraestructura del dominio de procesamiento de datos médicos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos en la capa de infraestructura del dominio de procesamiento de datos médicos

"""

from dataclasses import dataclass, field
from salud_tech.seedwork.dominio.fabricas import Fabrica
from salud_tech.seedwork.dominio.repositorios import Repositorio
from salud_tech.modulos.procesamiento.dominio.repositorios import RepositorioDatasetMedico
from .repositorios import RepositorioDatasetMedicoPostgres
from .excepciones import ExcepcionFabrica

@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        if obj == RepositorioDatasetMedico:
            return RepositorioDatasetMedicoPostgres()
        else:
            raise ExcepcionFabrica()
