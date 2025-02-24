from __future__ import annotations
from dataclasses import dataclass, field

import salud_tech.modulos.procesamiento.dominio.objetos_valor as ov
from salud_tech.seedwork.dominio.entidades import Entidad


@dataclass
class DatasetMedico(Entidad):
    registro_de_diagnostico: ov.RegistroDeDiagnostico = field(default_factory=ov.RegistroDeDiagnostico)    
    metadata: ov.Metadata = field(default_factory=ov.Metadata)
    estado: ov.Estado = field(default_factory=ov.Estado)

    def __str__(self) -> str:
        return self.estado.name.upper()

