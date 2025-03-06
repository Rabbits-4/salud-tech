from __future__ import annotations
from dataclasses import dataclass, field
from salud_tech.seedwork.dominio.eventos import EventoDominio
from salud_tech.modulos.procesamiento.dominio.objetos_valor import RegistroDeDiagnostico, Metadata
from datetime import datetime
import uuid

@dataclass
class DatasetCreado(EventoDominio):
    id_dataset: uuid.UUID = None
    estado: str = None
    fecha_creacion: datetime = None
    metadata: Metadata = None
    registro_de_diagnostico: RegistroDeDiagnostico = None