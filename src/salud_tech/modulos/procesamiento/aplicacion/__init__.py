from pydispatch import dispatcher

from .handlers import HandlerReservaIntegracion

from salud_tech.modulos.procesamiento.dominio.eventos import DatasetCreado

dispatcher.connect(HandlerReservaIntegracion.handle_crear_dataset_medico, signal=f'{DatasetCreado.__name__}Integracion')