from salud_tech.seedwork.aplicacion.comandos import ComandoHandler
from salud_tech.modulos.procesamiento.infraestructura.fabricas import FabricaRepositorio
from salud_tech.modulos.procesamiento.dominio.fabricas import FabricaProcesamiento

class CrearBaseHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_procesamiento: FabricaProcesamiento = FabricaProcesamiento()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_procesamiento(self):
        return self._fabrica_procesamiento
