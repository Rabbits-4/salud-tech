""" Interfaces para los repositorios del dominio de procesamiento de datos médicos

En este archivo usted encontrará las diferentes interfaces para repositorios
del dominio de procesamiento de datos médicos

"""

from abc import ABC, abstractmethod
from mapear.seedwork.dominio.repositorios import Repositorio
from .entidades import ParquetFile

class RepositorioParquet(Repositorio, ABC):
    
    @abstractmethod
    def obtener_por_id(self, id: str) -> ParquetFile:
        """Obtiene un Parquet por su ID"""
        pass

    @abstractmethod
    def agregar(self, dataset: ParquetFile) -> None:
        """Guarda un Parquet en el repositorio"""
        pass

    @abstractmethod
    def eliminar(self, id: str) -> None:
        """Elimina un Parquet del repositorio por su ID"""
        pass

    @abstractmethod
    def obtener_todos(self) -> list[ParquetFile]:
        """Obtiene todos los Parquet almacenados"""
        pass
