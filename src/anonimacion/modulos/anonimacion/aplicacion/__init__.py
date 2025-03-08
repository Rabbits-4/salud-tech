from pydispatch import dispatcher

from .handlers import HandlerDicomAnonimoIntegracion

from anonimacion.modulos.anonimacion.dominio.eventos import DicomAnonimizado

dispatcher.connect(HandlerDicomAnonimoIntegracion.handle_dicom_anonimo_creado, signal=f'{DicomAnonimizado.__name__}Integracion')
