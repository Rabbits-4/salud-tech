"""Objetos valor del dominio de anonimacion

En este archivo usted encontrará los objetos valor del dominio de anonimacion

"""

from __future__ import annotations

from dataclasses import dataclass, field
from anonimacion.seedwork.dominio.objetos_valor import ObjetoValor
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict

@dataclass
class EntornoClinico:
    tipo: str

@dataclass
class RegionAnatomica:
    nombre: str

@dataclass
class Modalidad:
    tipo: str

@dataclass
class Patologia:
    nombre: str

@dataclass
class RegistroDeDiagnostico:
    region_anatomica: RegionAnatomica
    modalidad: Modalidad
    patologia: Patologia

@dataclass
class NotasClinicas:
    descripcion: str

@dataclass
class ContextoProcesal:
    tipo: str

@dataclass
class Imagen:
    url: str
    descripcion: Optional[str] = ""

@dataclass
class Data:
    examenes: List[str]
    resultados: Dict[str, str]