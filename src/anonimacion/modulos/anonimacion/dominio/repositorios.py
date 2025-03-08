""" Interfaces para los repositorios del dominio de anonimacion de datos médicos

En este archivo usted encontrará las diferentes interfaces para repositorios
del dominio de anonimacion de datos médicos

"""

from abc import ABC, abstractmethod
from anonimacion.seedwork.dominio.repositorios import Repositorio
from .entidades import DicomAnonimo

class RepositorioDicomAnonimo(Repositorio, ABC):
    
    @abstractmethod
    def obtener_por_id(self, id: str) -> DicomAnonimo:
        """Obtiene un DicomAnonimo por su ID"""
        pass

    @abstractmethod
    def agregar(self, dataset: DicomAnonimo) -> None:
        """Guarda un DicomAnonimo en el repositorio"""
        pass

    @abstractmethod
    def eliminar(self, id: str) -> None:
        """Elimina un DicomAnonimo del repositorio por su ID"""
        pass

    @abstractmethod
    def obtener_todos(self) -> list[DicomAnonimo]:
        """Obtiene todos los DicomAnonimo almacenados"""
        pass
