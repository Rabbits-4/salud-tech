from pydispatch import dispatcher

from .handlers import HandlerParquetIntegracion

from mapear.modulos.procesamiento.dominio.eventos import DatasetCreado

dispatcher.connect(HandlerParquetIntegracion.handle_parquet_creado, signal=f'{DatasetCreado.__name__}Integracion')
