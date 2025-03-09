from mapear.seedwork.aplicacion.handlers import Handler
from mapear.modulos.mapear.infraestructura.despachadores import Despachador
from mapear.modulos.mapear.aplicacion.dto import ParquetDto
from mapear.modulos.mapear.dominio.fabricas import FabricaMapear
from mapear.modulos.mapear.infraestructura.fabricas import FabricaRepositorio
from mapear.modulos.mapear.aplicacion.mapeadores import MapeadorParquet
from mapear.modulos.mapear.infraestructura.repositorios import RepositorioParquet
import logging
from datetime import datetime 

class HandlerParquetIntegracion(Handler):
    
    @staticmethod
    def handle_parquet_creado(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'mapear.parquet.creado')

class HandlerCrearParquetDominio(Handler):
    @staticmethod
    def handle_crear_parquet(comando):
        parquet_dto = ParquetDto(
            entorno_clinico=comando["entorno_clinico"],
            registro_de_diagnostico=comando["registro_de_diagnostico"],
            fecha_creacion=datetime.now(),
            fecha_actualizacion=datetime.now(),
            historial_paciente_id=comando["historial_paciente_id"],
            contexto_procesal=comando["contexto_procesal"],
            notas_clinicas=comando["notas_clinicas"],
            data=comando["data"]
        )

        logging.error("🚀 Run handler by rest api")
        _fabrica_mapear: FabricaMapear = FabricaMapear()
        _fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()

        parquet: ParquetFile = _fabrica_mapear.crear_objeto(parquet_dto, MapeadorParquet())
        parquet.crear_parquet(parquet)

        repositorio_parquet = _fabrica_repositorio.crear_objeto(RepositorioParquet.__class__)

        repositorio_parquet.agregar(parquet)