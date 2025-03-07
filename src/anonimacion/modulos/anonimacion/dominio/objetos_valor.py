"""Objetos valor del dominio de anonimacion

En este archivo usted encontrará los objetos valor del dominio de anonimacion

"""

from __future__ import annotations

from dataclasses import dataclass, field
from anonimacion.seedwork.dominio.objetos_valor import ObjetoValor
from datetime import datetime
from enum import Enum

@dataclass(frozen=True)
class HistorialPacienteIdOriginal(ObjetoValor):
    historial_id: str
    condiciones_previas: list[str]

@dataclass(frozen=True)
class RegionAnatomica(ObjetoValor):
    nombre: str

@dataclass(frozen=True)
class Modalidad(ObjetoValor):
    tipo: str

@dataclass(frozen=True)
class Patologia(ObjetoValor):
    nombre: str

@dataclass(frozen=True)
class RegistroDeDiagnostico(ObjetoValor):
    region_anatomica: RegionAnatomica
    modalidad: Modalidad
    patologia: Patologia

@dataclass(frozen=True)
class EntornoClinico(ObjetoValor):
    tipo: str

@dataclass(frozen=True)
class NotasClinicas(ObjetoValor):
    descripcion: str

@dataclass(frozen=True)
class HistorialPaciente(ObjetoValor):
    historial_id: str
    condiciones_previas: list[str]

@dataclass(frozen=True)
class ContextoProcesal(ObjetoValor):
    tipo: str

@dataclass(frozen=True)
class Imagen(ObjetoValor):
    url: str
    descripcion: str

@dataclass(frozen=True)
class Metadata(ObjetoValor):
    entorno_clinico: EntornoClinico
    notas_clinicas: NotasClinicas
    historial_paciente: HistorialPaciente
    contexto_procesal: ContextoProcesal
    imagen: Imagen

class Estado(Enum):
    PENDIENTE = "Pendiente"
    EN_PROCESO = "En Proceso"
    FINALIZADO = "Finalizado"