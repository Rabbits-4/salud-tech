from mapear.seedwork.aplicacion.queries import QueryHandler
from mapear.modulos.procesamiento.infraestructura.fabricas import FabricaRepositorio
from mapear.modulos.procesamiento.dominio.fabricas import FabricaProcesamiento

class QueryBaseHandler(QueryHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_procesamiento: FabricaProcesamiento = FabricaProcesamiento()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_procesamiento(self):
        return self._fabrica_procesamiento
