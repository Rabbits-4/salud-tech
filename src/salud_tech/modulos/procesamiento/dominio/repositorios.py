""" Interfaces para los repositorios del dominio de procesamiento de datos médicos

En este archivo usted encontrará las diferentes interfaces para repositorios
del dominio de procesamiento de datos médicos

"""

from abc import ABC, abstractmethod
from salud_tech.seedwork.dominio.repositorios import Repositorio
from .entidades import Parcket

class RepositorioDatasetMedico(Repositorio, ABC):
    
    @abstractmethod
    def obtener_por_id(self, id: str) -> Parcket:
        """Obtiene un DatasetMedico por su ID"""
        pass

    @abstractmethod
    def agregar(self, dataset: Parcket) -> None:
        """Guarda un DatasetMedico en el repositorio"""
        pass

    @abstractmethod
    def eliminar(self, id: str) -> None:
        """Elimina un DatasetMedico del repositorio por su ID"""
        pass

    @abstractmethod
    def obtener_todos(self) -> list[Parcket]:
        """Obtiene todos los DatasetMedico almacenados"""
        pass
