from anonimacion.seedwork.aplicacion.handlers import Handler
from anonimacion.modulos.anonimacion.infraestructura.despachadores import Despachador

class HandlerDicomAnonimoIntegracion(Handler):
    
    @staticmethod
    def handle_dicom_anonimo_creado(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-dicom-anonimo')