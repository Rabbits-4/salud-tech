from anonimacion.seedwork.aplicacion.comandos import Comando
from datetime import datetime
from .base import CrearBaseHandler
from dataclasses import dataclass, field

from anonimacion.modulos.anonimacion.aplicacion.mapeadores import MapeadorDatasetAnonimo
from anonimacion.modulos.anonimacion.aplicacion.dto import DatasetAnonimoDto

from anonimacion.modulos.anonimacion.dominio.entidades import DatasetMedico
from anonimacion.seedwork.infraestructura.uow import UnidadTrabajoPuerto

from anonimacion.seedwork.aplicacion.comandos import ejecutar_commando

from anonimacion.modulos.anonimacion.infraestructura.repositorios import RepositorioDatasetAnonimo

@dataclass
class Anonimizar(Comando):
    historial_paciente_id_original: str,  
    img: str,
    entorno_clinico: str
    registro_de_diagnostico: dict
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    contexto_procesal: str
    notas_clinicas: str
    data: any

class AnonimizarHandler(CrearBaseHandler):

    def handle(self, comando: Anonimizar):

        dataset_anonimo_dto = DatasetAnonimoDto(
            packet_id=comando.packet_id,
            historial_paciente_id=comando.historial_paciente_id,
            img:comando.img,
            entorno_clinico=comando.entorno_clinico,
            registro_de_diagnostico=comando.registro_de_diagnostico,
            fecha_creacion=comando.fecha_creacion,
            fecha_actualizacion=comando.fecha_actualizacion,
            contexto_procesal=comando.contexto_procesal,
            notas_clinicas=comando.notas_clinicas,
            data=comando.data
        )

        dataset_anonimo: Dataset_Anonimo = self.fabrica_anonimacion.crear_objeto(dataset_anonimo_dto, MapeadorDatasetAnonimo())
        dataset_anonimo.anonimizar(dataset_anonimo)

        repositorio_dataset_anonimo = self.fabrica_repositorio.crear_objeto(RepositorioDatasetAnonimo.__class__)

        UnidadTrabajoPuerto.registrar_batch(repositorio_dataset_anonimo.agregar, dataset_anonimo)
        UnidadTrabajoPuerto.savepoint() # que hace?
        UnidadTrabajoPuerto.commit()

@ejecutar_commando.register(Anonimizar)
def ejecutar_commando_create_dataset_anonimo(comando: Anonimizar):
    handler = AnonimizarHandler()
    return handler.handle(comando)