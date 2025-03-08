from pydispatch import dispatcher

from .handlers import HandlerParquetIntegracion

from mapear.modulos.mapear.dominio.eventos import ParquetCreado

dispatcher.connect(HandlerParquetIntegracion.handle_parquet_creado, signal=f'{ParquetCreado.__name__}Integracion')
