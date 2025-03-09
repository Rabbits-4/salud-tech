from pulsar.schema import String, Long, Record
from salud_tech.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

class DatasetMedicoCreadoPayload(Record):
    id_dataset_medico = String()
    fecha_creacion = Long()

class EventoDatasetMedicoCreado(EventoIntegracion):
    data = DatasetMedicoCreadoPayload()

class ParquetCreadoPayload(Record):
    packet_id = String()
    entorno_clinico = String()
    registro_de_diagnostico = String()
    historial_paciente_id = String()
    fecha_creacion = String()
    fecha_actualizacion = String()
    contexto_procesal = String()
    notas_clinicas = String()
    data = String()

class EventoParquetCreado(EventoIntegracion):
    data = ParquetCreadoPayload()

class ProcesamientoIniciadoPayload(Record):
    id_saga = String()
    paso = String()

class ProcesamientoIniciado(EventoIntegracion):
    data = ProcesamientoIniciadoPayload()