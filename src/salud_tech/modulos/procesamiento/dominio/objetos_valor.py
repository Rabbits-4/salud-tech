"""Objetos valor del dominio de vuelos

En este archivo usted encontrará los objetos valor del dominio de vuelos

"""

from __future__ import annotations

from dataclasses import dataclass, field
from aeroalpes.seedwork.dominio.objetos_valor import ObjetoValor, Codigo, Ruta, Locacion
from datetime import datetime
from enum import Enum

@dataclass(frozen=True)
class RegionAnatomica(ObjetoValor):
    ...

@dataclass(frozen=True)
class Modalidad(ObjetoValor):
    ...

@dataclass(frozen=True)
class Patologia(ObjetoValor):
    ...

@dataclass(frozen=True)
class RegistroDeDiagnostico(ObjetoValor):
    region_anatomica: RegionAnatomica
    modalidad: Modalidad
    patologia: Patologia



@dataclass(frozen=True)
class EntornoClinico(ObjetoValor):
    ...

@dataclass(frozen=True)
class NotasClinicas(ObjetoValor):
    ...

@dataclass(frozen=True)
class HistorialPaciente(ObjetoValor):
    ...

@dataclass(frozen=True)
class ContextoProcesal(ObjetoValor):
    ...

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


@dataclass(frozen=True)
class Estado(ObjetoValor):
    name: str
