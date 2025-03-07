from anonimacion.seedwork.aplicacion.handlers import Handler
from anonimacion.modulos.anonimacion.infraestructura.despachadores import Despachador

class HandlerDatasetAnonimoIntegracion(Handler):
    
    @staticmethod
    def handle_dataset_anonimo_creado(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-dataset-anonimo')