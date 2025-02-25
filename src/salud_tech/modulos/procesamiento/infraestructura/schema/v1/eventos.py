from pulsar.schema import *
from salud_tech.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

class DatasetCreadoPayload(Record):
    id_dataset = String()
    estado = String()
    fecha_creacion = Long()

class EventoDatasetCreado(EventoIntegracion):
    data = DatasetCreadoPayload()
