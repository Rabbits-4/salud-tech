from mapear.seedwork.aplicacion.comandos import ComandoHandler
from mapear.modulos.mapear.infraestructura.fabricas import FabricaRepositorio
from mapear.modulos.mapear.dominio.fabricas import FabricaMapear

class CrearBaseHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_mapear: FabricaMapear = FabricaMapear()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_mapear(self):
        return self._fabrica_mapear
