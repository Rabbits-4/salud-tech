from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime

import mapear.modulos.mapear.dominio.objetos_valor as ov
from mapear.seedwork.dominio.entidades import AgregacionRaiz
from .eventos import ParquetCreado

@dataclass
class ParquetFile(AgregacionRaiz):
    registro_de_diagnostico: str
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    historial_paciente_id: str
    contexto_procesal: str
    notas_clinicas: str
    data: dict
    id: str
    estado: ov.Estado = field(default_factory=lambda: ov.Estado.EN_PROCESO)

    def crear_parquet(self, parquet: ParquetFile):

        self.agregar_evento(ParquetCreado(
            packet_id=self.id,
            fecha_creacion=parquet.fecha_creacion,
            fecha_actualizacion=parquet.fecha_actualizacion,
            historial_paciente_id=parquet.historial_paciente_id,
            registro_de_diagnostico=parquet.registro_de_diagnostico,
            contexto_procesal=parquet.contexto_procesal,
            notas_clinicas=parquet.notas_clinicas,
            data=parquet.data,
            estado=parquet.estado.value
        ))


    

