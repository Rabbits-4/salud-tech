from anonimacion.seedwork.aplicacion.comandos import Comando
from .base import CrearBaseHandler
from dataclasses import dataclass, field
from anonimacion.modulos.anonimacion.aplicacion.mapeadores import MapeadorDicomAnonimo
from anonimacion.modulos.anonimacion.aplicacion.dto import DicomAnonimoDto
from anonimacion.modulos.anonimacion.dominio.entidades import DicomAnonimo
from anonimacion.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from anonimacion.seedwork.aplicacion.comandos import ejecutar_commando
from anonimacion.modulos.anonimacion.infraestructura.repositorios import RepositorioDicomAnonimo
from anonimacion.modulos.anonimacion.infraestructura.despachadores import Despachador
from anonimacion.modulos.anonimacion.infraestructura.schema.v1.eventos import (
    AnonimacionIniciada, EventoDicomAnonimoCreado, AnonimacionIniciadaPayload
)
from datetime import datetime
import uuid
import logging


@dataclass
class Anonimizar(Comando):
    historial_paciente_id: str
    nombre_paciente: str
    direccion_paciente: str
    telefono_paciente: str
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
        
        # Mensaje de inicio saga
        id_saga = str(uuid.uuid4())
        self.publicar_evento_saga_log(id_saga, "  AnonimacionIniciada")

        # 1. Generar un token único para el paciente
        token_paciente = str(uuid.uuid4())

        # 2. Guardar la relación paciente-token en la base de datos (tabla privada)
        self.guardar_relacion_paciente(token_paciente, comando)

        # 3. Crear un DTO sin los datos sensibles
        dicom_anonimo_dto = DicomAnonimoDto(
            packet_id=token_paciente,
            imagen=comando.img,
            entorno_clinico=comando.entorno_clinico,
            registro_de_diagnostico=comando.registro_de_diagnostico,
            fecha_creacion=comando.fecha_creacion,
            fecha_actualizacion=comando.fecha_actualizacion,
            contexto_procesal=comando.contexto_procesal,
            notas_clinicas=comando.notas_clinicas,
            data=comando.data
        )

        # 4. Mapear el DTO a la entidad de dominio
        dicom_anonimo: DicomAnonimo = MapeadorDicomAnonimo().dto_a_entidad(dicom_anonimo_dto)

        # 5. Persistir el DicomAnonimo en la base de datos
        repositorio_dicom_anonimo = self.fabrica_repositorio.crear_objeto(RepositorioDicomAnonimo.__class__)

        UnidadTrabajoPuerto.registrar_batch(repositorio_dicom_anonimo.agregar, dicom_anonimo)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()

        # 6. Publicar el evento con el Dicom Anonimizado
        self.publicar_evento_dicom_anonimizado(dicom_anonimo)

        self.publicar_evento_saga_log(id_saga, "  DicomAnonimizado")

    def guardar_relacion_paciente(self, token_paciente, comando):
        """
        Guarda la relación entre el token generado y los datos originales del paciente
        en una tabla privada a la que solo el microservicio de anonimización tiene acceso.
        """
        from anonimacion.config.db import db
        db.session.execute(
            "INSERT INTO relaciones_pacientes (token, historial_paciente_id, nombre, direccion, telefono) VALUES (:token, :historial_paciente_id, :nombre, :direccion, :telefono)",
            {"token": token_paciente, "historial_paciente_id": comando.historial_paciente_id, "nombre": comando.nombre_paciente, "direccion": comando.direccion_paciente, "telefono": comando.telefono_paciente}
        )
        db.session.commit()

    def publicar_evento_dicom_anonimizado(self, dicom_anonimo):
        despachador = Despachador()
        """
        Publica un evento con el DicomAnonimo ya anonimizado para que sea procesado en la siguiente fase.
        """
        despachador.publicar_evento(dicom_anonimo)

    def publicar_evento_saga_log(self, id_saga, paso, topico="eventos-saga"):
        """ 
        Publica un evento en Pulsar y lo registra en el log.
        """
        despachador = Despachador()
        evento = AnonimacionIniciadaPayload(
            id_saga=id_saga,
            paso=paso
        )
        
        logging.info(f"📡 [ANONIMIZACION] Publicado evento `{paso}` con id `{id_saga}` en `{topico}`")
        despachador.publicar_evento_saga(evento)
        
@ejecutar_commando.register(Anonimizar)
def ejecutar_commando_anonimizar(comando: Anonimizar):
    handler = AnonimizarHandler()
    return handler.handle(comando)