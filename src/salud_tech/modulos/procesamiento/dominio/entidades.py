from __future__ import annotations
from dataclasses import dataclass, field

import salud_tech.modulos.procesamiento.dominio.objetos_valor as ov

from salud_tech.seedwork.dominio.entidades import AgregacionRaiz

from .eventos import DatasetCreado


@dataclass
class DatasetMedico(AgregacionRaiz):
    registro_de_diagnostico: ov.RegistroDeDiagnostico = field(default_factory=ov.RegistroDeDiagnostico)    
    metadata: ov.Metadata = field(default_factory=ov.Metadata)
    estado: ov.Estado = field(default_factory=ov.Estado)

    def creat_dataset(self, dataset: DatasetMedico):
        self.registro_de_diagnostico = dataset.registro_de_diagnostico
        self.metadata = dataset.metadata
        self.estado = dataset.estado

        self.agregar_evento(DatasetCreado(
            id=self.id,
            estado=self.estado.name,
            fecha_creacion=self.fecha_creacion,
            metadata=self.metadata,
            registro_de_diagnostico=self.registro_de_diagnostico            
        ))

    

