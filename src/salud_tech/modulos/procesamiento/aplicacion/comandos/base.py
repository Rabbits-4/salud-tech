from salud_tech.seedwork.aplicacion.comandos import ComandoHandler
from salud_tech.modulos.vuelos.infraestructura.fabricas import FabricaRepositorio
from salud_tech.modulos.vuelos.dominio.fabricas import FabricaVuelos

class CrearBaseHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_procesamiento: FabricaVuelos = FabricaVuelos()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_procesamiento(self):
        return self._fabrica_procesamiento
    