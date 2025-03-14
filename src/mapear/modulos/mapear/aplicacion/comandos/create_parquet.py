from mapear.seedwork.aplicacion.comandos import Comando
from datetime import datetime
from .base import CrearBaseHandler
from dataclasses import dataclass
import json
import logging
import uuid

from mapear.modulos.mapear.aplicacion.mapeadores import MapeadorParquet
from mapear.modulos.mapear.aplicacion.dto import ParquetDto
from mapear.modulos.mapear.dominio.entidades import ParquetFile
from mapear.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from mapear.seedwork.aplicacion.comandos import ejecutar_commando
from mapear.modulos.mapear.infraestructura.repositorios import RepositorioParquet
from mapear.modulos.mapear.infraestructura.despachadores import Despachador
from mapear.modulos.mapear.infraestructura.schema.v1.eventos import ( 
    EventoParquetCreado, ParquetCreadoPayload,
    MapeoIniciado, MapeoIniciadoPayload 
)

@dataclass
class CreateParquet(Comando):
    entorno_clinico: str
    registro_de_diagnostico: dict
    historial_paciente_id: str
    contexto_procesal: str
    notas_clinicas: str
    data: dict

    def to_dict(self):
        return {
            "entorno_clinico": self.entorno_clinico,
            "registro_de_diagnostico": self.registro_de_diagnostico,
            "historial_paciente_id": self.historial_paciente_id,
            "contexto_procesal": self.contexto_procesal,
            "notas_clinicas": self.notas_clinicas,
            "data": self.data
        }

class CrearParquetHandler(CrearBaseHandler):

    def handle(self, comando: CreateParquet):        

        id_saga = str(uuid.uuid4())
        self.publicar_evento_saga_log(id_saga, "MapeoIniciado")

        if comando.entorno_clinico == "FalloSimuladoMapear":
            logging.error("❌ [Mapear] Error simulado detectado. Publicando evento de error en la saga.")
            self.publicar_evento_saga_log(id_saga, "  MapeoFallido")
            return  

        parquet_dto = ParquetDto(
            entorno_clinico=comando.entorno_clinico,
            registro_de_diagnostico=json.dumps(comando.registro_de_diagnostico),  
            fecha_creacion=datetime.now(),
            fecha_actualizacion=datetime.now(),
            historial_paciente_id=comando.historial_paciente_id,
            contexto_procesal=comando.contexto_procesal,
            notas_clinicas=comando.notas_clinicas,
            data=json.dumps(comando.data)  
        )

        parquet: ParquetFile = self.fabrica_mapear.crear_objeto(parquet_dto, MapeadorParquet())

        parquet.crear_parquet(parquet)

        repositorio_parquet = self.fabrica_repositorio.crear_objeto(RepositorioParquet.__class__)

        from mapear.config.uow import UnidadTrabajoSQLAlchemy
        from mapear.config.db import db
        from mapear.api import create_app

        app = create_app({"TESTING": True})  # 🔹 Creamos la instancia de Flask para contexto

        with app.app_context():
            try:
                with UnidadTrabajoSQLAlchemy() as uow:
                    repositorio_parquet.agregar(parquet)
                    uow.commit()
                
            except Exception as e:
                logging.error(f"❌ [MAPEO] Error guardando Parquet en BD: {e}")
                raise e
            finally:
                db.session.close()
                logging.info("🚀 db session cerrada exitosamente")

            # 📡 **Publicar evento de integración en Pulsar**
            try:
                despachador = Despachador()
                despachador.publicar_evento(parquet, "parquet-creado")
                self.publicar_evento_saga_log(id_saga, "ParquetMapeado")
                
            except Exception as e:
                logging.error(f"❌ [MAPEO] Error publicando evento `parquet-creado`: {e}")
   
    def publicar_evento_saga_log(self, id_saga, paso, topico="eventos-saga"):
        """ 
        Publica un evento en Pulsar y lo registra en el log.
        """
        despachador = Despachador()
        evento = MapeoIniciadoPayload(
            id_saga=id_saga,
            paso=paso
        )
        
        logging.info(f"📡 [ANONIMIZACION] Publicado evento `{paso}` con id `{id_saga}` en `{topico}`")
        despachador.publicar_evento_saga(evento)

@ejecutar_commando.register(CreateParquet)
def ejecutar_commando_create_parquet(comando: CreateParquet):
    handler = CrearParquetHandler()
    return handler.handle(comando)
