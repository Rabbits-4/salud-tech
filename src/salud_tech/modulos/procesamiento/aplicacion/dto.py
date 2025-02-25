from dataclasses import dataclass, field
from salud_tech.seedwork.aplicacion.dto import DTO
from datetime import datetime
from typing import Optional, Dict

@dataclass(frozen=True)
class MetadataDto(DTO):
    registro_de_diagnostico: Dict = field(default_factory=dict)
    fecha_creacion: datetime = field(default_factory=datetime.now)
    fecha_actualizacion: datetime = field(default_factory=datetime.now)
    historial_paciente_id: str = field(default_factory=str)
    contexto_procesal: str = field(default_factory=str)
    notas_clinicas: str = field(default_factory=str)

@dataclass(frozen=True)
class DatasetMedicoDto(DTO):
    packet_id: str = field(default_factory=str)
    entorno_clinico: str = field(default_factory=str)
    metadata: MetadataDto
    data: Optional[Dict] = field(default_factory=dict)
