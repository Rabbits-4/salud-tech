"""Reglas de negocio del dominio de procesamiento de datos médicos

En este archivo usted encontrará reglas de negocio del dominio de procesamiento de datos médicos

"""

from anonimacion.seedwork.dominio.reglas import ReglaNegocio

class ImagenConUrlValida(ReglaNegocio):    
    url: str

    def __init__(self, url, mensaje='La URL de la imagen no es válida'):
        super().__init__(mensaje)
        self.url = url

    def es_valido(self) -> bool:
        return self.url.startswith('http')

