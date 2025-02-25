from salud_tech.modulos.procesamiento.dominio.eventos import DatasetCreado
from salud_tech.seedwork.aplicacion.handlers import Handler
from salud_tech.modulos.procesamiento.infraestructura.despachadores import Despachador

class HandlerDatasetMedicoIntegracion(Handler):
    
    @staticmethod
    def handle_crear_dataset_medico(evento: DatasetCreado):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-dataset-medico')