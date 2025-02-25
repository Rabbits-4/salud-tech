"""Reglas de negocio del dominio de cliente

En este archivo usted encontrará reglas de negocio del dominio de cliente

"""

from aeroalpes.seedwork.dominio.reglas import ReglaNegocio
from .objetos_valor import Ruta
from .entidades import Pasajero
from .objetos_valor import TipoPasajero, Itinerario


class ImgenConUrlValida(ReglaNegocio):    
    url: str

    def __init__(self, url, mensaje='La url de la imagen no es válida'):
        super().__init__(mensaje)
        self.url = url

    def es_valido(self) -> bool:
        return self.url.startswith('http')


    itinerarios: list[Itinerario]

    def __init__(self, itinerarios, mensaje='La lista de itinerarios debe tener al menos un itinerario'):
        super().__init__(mensaje)
        self.itinerarios = itinerarios

    def es_valido(self) -> bool:
        return len(self.itinerarios) > 0 and isinstance(self.itinerarios[0], Itinerario) 