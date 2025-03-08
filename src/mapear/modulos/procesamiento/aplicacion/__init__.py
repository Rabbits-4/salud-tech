from pydispatch import dispatcher

from .handlers import HandlerDatasetMedicoIntegracion

from mapear.modulos.procesamiento.dominio.eventos import DatasetCreado

dispatcher.connect(HandlerDatasetMedicoIntegracion.handle_dataset_medico_creado, signal=f'{DatasetCreado.__name__}Integracion')
