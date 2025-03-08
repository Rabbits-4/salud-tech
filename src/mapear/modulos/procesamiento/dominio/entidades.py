from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime

import mapear.modulos.procesamiento.dominio.objetos_valor as ov
from mapear.seedwork.dominio.entidades import AgregacionRaiz
from .eventos import ParquetCreado

@dataclass
class ParquetFile(AgregacionRaiz):
    id: str
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    registro_de_diagnostico: str
    contexto_procesal: str
    notas_clinicas: str
    data: dict
    estado: ov.Estado = field(default_factory=lambda: ov.Estado.EN_PROCESO)

    def crear_parquet(self, dataset: ParquetFile):

        self.agregar_evento(ParquetCreado(
            packet_id=self.id,
            fecha_creacion=dataset.fecha_creacion,
            fecha_actualizacion=dataset.fecha_actualizacion,
            registro_de_diagnostico=dataset.registro_de_diagnostico,
            contexto_procesal=dataset.contexto_procesal,
            notas_clinicas=dataset.notas_clinicas,
            data=dataset.data,
            estado=dataset.estado.value
        ))


    

