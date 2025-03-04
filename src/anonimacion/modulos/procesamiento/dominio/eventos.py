from __future__ import annotations
from dataclasses import dataclass, field
from salud_tech.seedwork.dominio.eventos import EventoDominio
from salud_tech.modulos.procesamiento.dominio.objetos_valor import RegistroDeDiagnostico, Metadata
from datetime import datetime
import uuid

@dataclass
class ParcketCreado(EventoDominio):
    id: uuid.UUID = None
    fecha_creacion: str = None
    entorno_clinico: str = None
    registro_de_diagnostico: str = None
    fecha_creacion: str = None
    fecha_actualizacion: str = None
    historial_paciente_id: str = None
    contexto_procesal: str = None
    notas_clinicas: str = None
    data: dict = None