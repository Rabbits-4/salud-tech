from dataclasses import dataclass, field
from aeroalpes.seedwork.aplicacion.dto import DTO
from datetime import datetime

@dataclass(frozen=True)
class MetadataDto(DTO):
    registro_de_diagnostico: dict = field(default_factory=dict)
    fecha_creacion: datetime = field(default_factory=datetime)
    fecha_actualizacion: datetime = field(default_factory=datetime)
    historial_paciente_id: str = field(default_factory=str)
    contexto_procesal: str = field(default_factory=str)
    notas_clinicas: str = field(default_factory=str)

@dataclass(frozen=True)
class DatasetMedicoDto(DTO):
    packet_id: str = field(default_factory=str)
    entorno_clinico: str = field(default_factory=str)
    metadata: MetadataDto
    data: any = field(default_factory=dict)


