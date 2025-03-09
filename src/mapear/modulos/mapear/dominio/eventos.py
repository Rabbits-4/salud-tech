from __future__ import annotations
from dataclasses import dataclass, field
from mapear.seedwork.dominio.eventos import EventoDominio
from datetime import datetime
import uuid

@dataclass
class ParquetCreado(EventoDominio):
    id: uuid.UUID
    fecha_creacion: datetime = None
    fecha_actualizacion: datetime = None
    historial_paciente_id: str = None
    contexto_procesal: str = None
    notas_clinicas: str = None
    registro_de_diagnostico: dict = None
    entorno_clinico: str = None
    data: dict = None
    estado: str = None    
    