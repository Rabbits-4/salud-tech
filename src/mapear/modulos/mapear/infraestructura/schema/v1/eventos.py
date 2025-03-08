from pulsar.schema import String, Long, Record
from mapear.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

class ParquetCreadoPayload(Record):
    id_dataset_medico = String()
    fecha_creacion = Long()

class EventoParquetCreado(EventoIntegracion):
    data = ParquetCreadoPayload()