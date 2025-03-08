from __future__ import annotations
from dataclasses import dataclass, field
from anonimacion.seedwork.dominio.eventos import EventoDominio
import anonimacion.modulos.anonimacion.dominio.objetos_valor as ov
from datetime import datetime
import uuid

@dataclass
class DicomAnonimizado(EventoDominio):
    id: uuid.UUID
    token: uuid.UUID = None
    imagen: ov.Imagen = None
    entorno_clinico: ov.EntornoClinico = None
    registro_de_diagnostico: Optional[ov.RegistroDeDiagnostico] = field(default=None)
    fecha_creacion: datetime = None
    fecha_actualizacion: datetime = None
    contexto_procesal: ov.ContextoProcesal = None


    notas_clinicas: Optional[ov.NotasClinicas] = field(default=None)
    data: Optional[ov.Data] = field(default=None)