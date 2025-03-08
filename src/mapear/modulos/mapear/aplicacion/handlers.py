from mapear.seedwork.aplicacion.handlers import Handler
from mapear.modulos.mapear.infraestructura.despachadores import Despachador

class HandlerParquetIntegracion(Handler):
    
    @staticmethod
    def handle_parquet_creado(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'mapear.parquet.creado')