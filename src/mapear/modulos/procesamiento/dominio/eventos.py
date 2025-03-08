from __future__ import annotations
from dataclasses import dataclass, field
from mapear.seedwork.dominio.eventos import EventoDominio
from mapear.modulos.procesamiento.dominio.objetos_valor import RegistroDeDiagnostico, Metadata
from datetime import datetime
import uuid

@dataclass
class ParquetCreado(EventoDominio):
    packet_id: uuid.UUID = None
    fecha_creacion: datetime = None
    fecha_actualizacion: datetime = None
    registro_de_diagnostico: RegistroDeDiagnostico = None
    contexto_procesal: str = None
    notas_clinicas: str = None
    data: dict = None
    estado: str = None    
    