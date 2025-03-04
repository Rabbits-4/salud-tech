from pulsar.schema import String, Long, Record
from salud_tech.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

class DatasetMedicoCreadoPayload(Record):
    id_dataset_medico = String()
    fecha_creacion = Long()

class EventoDatasetMedicoCreado(EventoIntegracion):
    data = DatasetMedicoCreadoPayload()