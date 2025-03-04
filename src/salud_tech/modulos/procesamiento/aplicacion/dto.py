from dataclasses import dataclass, field
from salud_tech.seedwork.aplicacion.dto import DTO

@dataclass(frozen=True)
class ParquetDto(DTO):
    entorno_clinico: str = field(default_factory=str),
    registro_de_diagnostico=field(default_factory=str),
    historial_paciente_id=field(default_factory=str),
    contexto_procesal=field(default_factory=str),
    notas_clinicas=field(default_factory=str),            
    data=field(default_factory=dict)
