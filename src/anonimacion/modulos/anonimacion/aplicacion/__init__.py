from pydispatch import dispatcher

from .handlers import HandlerDatasetAnonimoIntegracion

from anonimacion.modulos.anonimacion.dominio.eventos import AnonimacionRealizada

dispatcher.connect(HandlerDatasetAnonimoIntegracion.handle_dataset_anonimo_creado, signal=f'{AnonimacionRealizada.__name__}Integracion')
