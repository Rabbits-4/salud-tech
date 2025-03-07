from anonimacion.seedwork.aplicacion.comandos import Comando
from datetime import datetime
from .base import CrearBaseHandler
from dataclasses import dataclass, field

from anonimacion.modulos.anonimacion.aplicacion.mapeadores import MapeadorDicomAnonimo
from anonimacion.modulos.anonimacion.aplicacion.dto import DicomAnonimoDto

from anonimacion.modulos.anonimacion.dominio.entidades import DicomAnonimo
from anonimacion.seedwork.infraestructura.uow import UnidadTrabajoPuerto

from anonimacion.seedwork.aplicacion.comandos import ejecutar_commando

from anonimacion.modulos.anonimacion.infraestructura.repositorios import RepositorioDicomAnonimo

@dataclass
class Anonimizar(Comando):
    img: str
    entorno_clinico: str
    registro_de_diagnostico: dict
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    contexto_procesal: str
    notas_clinicas: str
    data: any

class AnonimizarHandler(CrearBaseHandler):

    def handle(self, comando: Anonimizar):

        dicom_anonimo_dto = DicomAnonimoDto(
            imagen=comando.img,
            entorno_clinico=comando.entorno_clinico,
            registro_de_diagnostico=comando.registro_de_diagnostico,
            fecha_creacion=comando.fecha_creacion,
            fecha_actualizacion=comando.fecha_actualizacion,
            contexto_procesal=comando.contexto_procesal,
            notas_clinicas=comando.notas_clinicas,
            data=comando.data
        )

        dicom_anonimo: DicomAnonimo = self.fabrica_anonimacion.crear_objeto(dicom_anonimo_dto, MapeadorDicomAnonimo())
        dicom_anonimo.anonimizar()

        repositorio_dicom_anonimo = self.fabrica_repositorio.crear_objeto(RepositorioDicomAnonimo.__class__)

        UnidadTrabajoPuerto.registrar_batch(repositorio_dicom_anonimo.agregar, dicom_anonimo)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()

@ejecutar_commando.register(Anonimizar)
def ejecutar_commando_anonimizar(comando: Anonimizar):
    handler = AnonimizarHandler()
    return handler.handle(comando)