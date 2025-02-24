from __future__ import annotations
from dataclasses import dataclass, field
from salud_tech.seedwork.dominio.eventos import (EventoDominio)
from salud_tech.modulos.procesamiento.dominio.objetos_valor import (RegistroDeDiagnostico, Metadata as OvMetadata)
from datetime import datetime
import uuid

@dataclass
class ReservaCreada(EventoDominio):
    id_reserva: uuid.UUID = None
    id_cliente: uuid.UUID = None
    estado: str = None
    fecha_creacion: datetime = None
    
@dataclass
class ReservaCancelada(EventoDominio):
    id_reserva: uuid.UUID = None
    fecha_actualizacion: datetime = None

@dataclass
class ReservaAprobada(EventoDominio):
    id_reserva: uuid.UUID = None
    fecha_actualizacion: datetime = None

@dataclass
class ReservaPagada(EventoDominio):
    id_reserva: uuid.UUID = None
    fecha_actualizacion: datetime = None

@dataclass
class DatasetCreado(EventoDominio):
    id_dataset: uuid.UUID = None
    estado: str = None
    fecha_creacion: datetime = None

@dataclass
class Metadata(OvMetadata):
    ...    


@dataclass
class DatasetCreado(EventoDominio):
    id_dataset: uuid.UUID = None
    estado: str = None
    fecha_creacion: datetime = None
    metadata: Metadata = None
    registro_de_diagnostico: dict = None


    