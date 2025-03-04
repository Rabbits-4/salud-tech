from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

import salud_tech.modulos.procesamiento.dominio.objetos_valor as ov
from salud_tech.seedwork.dominio.entidades import AgregacionRaiz
from .eventos import DatasetCreado

@dataclass
class DatasetMedico(AgregacionRaiz):
    id: str
    fecha_creacion: str
    registro_de_diagnostico: Optional[ov.RegistroDeDiagnostico] = None    
    metadata: Optional[ov.Metadata] = None
    estado: ov.Estado = field(default_factory=lambda: ov.Estado.PENDIENTE)

    def crear_dataset(self, dataset: DatasetMedico):
        self.registro_de_diagnostico = dataset.registro_de_diagnostico
        self.metadata = dataset.metadata
        self.estado = dataset.estado

        self.agregar_evento(DatasetCreado(
            id=self.id,
            estado=self.estado.nombre if hasattr(self.estado, 'nombre') else str(self.estado),
            fecha_creacion=self.fecha_creacion,
            metadata=self.metadata,
            registro_de_diagnostico=self.registro_de_diagnostico            
        ))


    

