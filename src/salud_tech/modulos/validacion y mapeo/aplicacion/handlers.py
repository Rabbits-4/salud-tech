from salud_tech.seedwork.aplicacion.handlers import Handler
from salud_tech.modulos.procesamiento.infraestructura.despachadores import Despachador

class HandlerDatasetMedicoIntegracion(Handler):
    
    @staticmethod
    def handle_dataset_medico_creado(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-dataset-medico')