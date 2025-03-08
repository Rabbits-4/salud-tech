from mapear.seedwork.aplicacion.queries import QueryHandler
from mapear.modulos.mapear.infraestructura.fabricas import FabricaRepositorio
from mapear.modulos.mapear.dominio.fabricas import FabricaMapear

class QueryBaseHandler(QueryHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_mapear: FabricaMapear = FabricaMapear()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_mapear(self):
        return self._fabrica_mapear
