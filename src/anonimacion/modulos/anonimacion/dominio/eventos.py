from __future__ import annotations
from dataclasses import dataclass, field
from anonimacion.seedwork.dominio.eventos import EventoDominio
import anonimacion.modulos.anonimacion.dominio.objetos_valor as ov
from datetime import datetime
import uuid

@dataclass
class DicomAnonimizado(EventoDominio):
    id: uuid.UUID
    token: uuid.UUID
    imagen: ov.Imagen
    entorno_clinico: ov.EntornoClinico
    registro_de_diagnostico: Optional[ov.RegistroDeDiagnostico]
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    contexto_procesal: ov.ContextoProcesal
    notas_clinicas: Optional[ov.NotasClinicas] = None
    data: Optional[ov.Data] = None