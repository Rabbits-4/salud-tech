""" Excepciones del dominio de procesamiento de datos médicos

En este archivo usted encontrará las excepciones relacionadas
al dominio de procesamiento de datos médicos

"""

from mapear.seedwork.dominio.excepciones import ExcepcionFabrica

class TipoObjetoNoExisteEnDominioProcesamientoExcepcion(ExcepcionFabrica):
    def __init__(self, mensaje='No existe una fábrica para el tipo solicitado en el módulo de procesamiento de datos médicos'):
        self.__mensaje = mensaje
    def __str__(self):
        return str(self.__mensaje)