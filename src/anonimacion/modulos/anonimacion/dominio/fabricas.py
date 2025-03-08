""" Fábricas para la creación de objetos del dominio de Anonimacion de datos médicos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos del dominio de Anonimacion de datos médicos

"""

from .entidades import DicomAnonimo
from .excepciones import TipoObjetoNoExisteEnDominioAnonimacionExcepcion
from anonimacion.seedwork.dominio.repositorios import Mapeador, Repositorio
from anonimacion.seedwork.dominio.fabricas import Fabrica
from anonimacion.seedwork.dominio.entidades import Entidad
from dataclasses import dataclass

@dataclass
class _FabricaDicomAnonimo(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad):
            return mapeador.entidad_a_dto(obj)
        else:
            dicom_anonimo: DicomAnonimo = mapeador.dto_a_entidad(obj)
            return dicom_anonimo

@dataclass
class FabricaAnonimacion(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == DicomAnonimo.__class__:
            fabrica_dicom_anonimo = _FabricaDicomAnonimo()
            return fabrica_dicom_anonimo.crear_objeto(obj, mapeador)
        else:
            raise TipoObjetoNoExisteEnDominioAnonimacionExcepcion()
