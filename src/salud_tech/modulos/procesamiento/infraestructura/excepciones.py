""" Excepciones para la capa de infraestructura del dominio de procesamiento de datos médicos

En este archivo usted encontrará las Excepciones relacionadas
a la capa de infraestructura del dominio de procesamiento de datos médicos

"""

from salud_tech.seedwork.dominio.excepciones import ExcepcionFabrica

class NoExisteImplementacionParaTipoFabricaExcepcion(ExcepcionFabrica):
    def __init__(self, mensaje='No existe una implementación para el repositorio con el tipo dado.'):
        self.__mensaje = mensaje
    def __str__(self):
        return str(self.__mensaje)