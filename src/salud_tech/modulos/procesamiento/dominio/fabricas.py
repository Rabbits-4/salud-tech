""" Fábricas para la creación de objetos del dominio de vuelos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos del dominio de vuelos

"""

from .entidades import DatasetMedico
from .reglas import MinimoUnItinerario, RutaValida 
from .excepciones import TipoObjetoNoExisteEnDominioVuelosExcepcion
from salud_tech.seedwork.dominio.repositorios import Mapeador, Repositorio
from salud_tech.seedwork.dominio.fabricas import Fabrica
from salud_tech.seedwork.dominio.entidades import Entidad
from dataclasses import dataclass

@dataclass
class _FabricaDatasetMedico(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad):
            return mapeador.entidad_a_dto(obj)
        else:
            dataset_medico: DatasetMedico = mapeador.dto_a_entidad(obj)

            self.validar_regla(ImgenConUrlValida(dataset_medico.image))            
            
            return dataset_medico

@dataclass
class FabricaProcesamiento(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == DatasetMedico.__class__:
            fabrica_reserva = _FabricaDatasetMedico()
            return fabrica_reserva.crear_objeto(obj, mapeador)
        else:
            raise TipoObjetoNoExisteEnDominioVuelosExcepcion()

