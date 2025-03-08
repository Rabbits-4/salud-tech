"""Objetos valor del dominio de procesamiento médico

En este archivo usted encontrará los objetos valor del dominio de procesamiento médico

"""

from __future__ import annotations

from enum import Enum

class Estado(Enum):
    PENDIENTE = "Pendiente"
    EN_PROCESO = "En Proceso"
    FINALIZADO = "Finalizado"