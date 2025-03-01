from salud_tech.seedwork.aplicacion.handlers import Handler
from salud_tech.modulos.procesamiento.infraestructura.despachadores import Despachador

class HandlerDatasetMedicoIntegracion(Handler):
    
    @staticmethod
    def handle_crear_dataset_medico(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-dataset-medico')