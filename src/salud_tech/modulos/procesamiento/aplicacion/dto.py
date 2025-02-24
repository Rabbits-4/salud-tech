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
class DatasetDto(DTO):
    packet_id: str = field(default_factory=str)
    entorno_clinico: str = field(default_factory=str)
    metadata: MetadataDto
    data: any = field(default_factory=dict)

@dataclass(frozen=True)
class LegDTO(DTO):
    fecha_salida: str
    fecha_llegada: str
    origen: dict
    destino: dict

@dataclass(frozen=True)
class SegmentoDTO(DTO):
    legs: list[LegDTO]

@dataclass(frozen=True)
class OdoDTO(DTO):
    segmentos: list[SegmentoDTO]

@dataclass(frozen=True)
class ItinerarioDTO(DTO):
    odos: list[OdoDTO]

@dataclass(frozen=True)
class ReservaDTO(DTO):
    fecha_creacion: str = field(default_factory=str)
    fecha_actualizacion: str = field(default_factory=str)
    id: str = field(default_factory=str)
    itinerarios: list[ItinerarioDTO] = field(default_factory=list)

@dataclass(frozen=True)
class DatasetMedicoDTO(DTO):
    metadata: dict
    id: str = field(default_factory=str)
