from anonimacion.seedwork.aplicacion.queries import QueryHandler
from anonimacion.modulos.anonimacion.infraestructura.fabricas import FabricaRepositorio
from anonimacion.modulos.anonimacion.dominio.fabricas import FabricaAnonimacion

class QueryBaseHandler(QueryHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_anonimacion: FabricaAnonimacion = FabricaAnonimacion()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_anonimacion(self):
        return self._fabrica_anonimacion
