from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime

import mapear.modulos.mapear.dominio.objetos_valor as ov
from mapear.seedwork.dominio.entidades import AgregacionRaiz
from .eventos import ParquetCreado

import logging
import json

@dataclass
class ParquetFile(AgregacionRaiz):
    id: str
    fecha_creacion: datetime = field(default_factory=datetime.now)
    fecha_actualizacion: datetime = field(default_factory=datetime.now)
    historial_paciente_id: str = None
    contexto_procesal: str = None
    registro_de_diagnostico: str = None
    entorno_clinico: str = None
    notas_clinicas: str = None
    data: dict = field(default_factory=dict)
    estado: ov.Estado = field(default_factory=lambda: ov.Estado.EN_PROCESO)

    def crear_parquet(self, parquet: ParquetFile):

        self.agregar_evento(ParquetCreado(
            packet_id=self.id,
            fecha_creacion=parquet.fecha_creacion.isoformat(),
            fecha_actualizacion=parquet.fecha_actualizacion.isoformat(),
            historial_paciente_id=parquet.historial_paciente_id,
            contexto_procesal=parquet.contexto_procesal,
            notas_clinicas=parquet.notas_clinicas,
            registro_de_diagnostico=parquet.registro_de_diagnostico,
            entorno_clinico=parquet.entorno_clinico,
            data=json.dumps(parquet.data),
            estado=parquet.estado.value
        ))


    

