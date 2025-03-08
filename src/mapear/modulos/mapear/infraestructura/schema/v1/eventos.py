from pulsar.schema import String, Long, Record
from mapear.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

class ParquetCreadoPayload(Record):
    packet_id = String()
    fecha_creacion = String()
    fecha_actualizacion = String()
    registro_de_diagnostico = String()
    entorno_clinico = String()
    historial_paciente_id = String()
    contexto_procesal = String()
    notas_clinicas = String()
    data = String()
    estado = String()

    

class EventoParquetCreado(EventoIntegracion):
    data = ParquetCreadoPayload()