""" Excepciones del dominio de anonimacion de datos médicos

En este archivo usted encontrará las excepciones relacionadas
al dominio de anonimacion de datos médicos

"""

from anonimacion.seedwork.dominio.excepciones import ExcepcionFabrica

class TipoObjetoNoExisteEnDominioAnonimacionExcepcion(ExcepcionFabrica):
    def __init__(self, mensaje='No existe una fábrica para el tipo solicitado en el módulo de anonimacion de datos médicos'):
        self.__mensaje = mensaje
    def __str__(self):
        return str(self.__mensaje)