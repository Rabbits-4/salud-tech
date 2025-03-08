from dataclasses import dataclass, field
from anonimacion.seedwork.aplicacion.dto import DTO
from datetime import datetime
from typing import Optional, Dict

@dataclass(frozen=True)
class DicomAnonimoDto(DTO):
    packet_id: str = field(default_factory=str)

    # Datos del paciente (para el proceso de anonimización)
    historial_paciente_id: str = field(default_factory=str)
    nombre_paciente: str = field(default_factory=str)
    direccion_paciente: str = field(default_factory=str)
    telefono_paciente: str = field(default_factory=str)

    # Datos del DICOM
    imagen: str = field(default_factory=str)
    entorno_clinico: str = field(default_factory=str)
    registro_de_diagnostico: Dict = field(default_factory=dict)
    fecha_creacion: datetime = field(default_factory=datetime.now)
    fecha_actualizacion: datetime = field(default_factory=datetime.now)
    contexto_procesal: str = field(default_factory=str)
    notas_clinicas: str = field(default_factory=str)
    data: Optional[Dict] = field(default_factory=dict)
