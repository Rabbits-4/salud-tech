from pulsar.schema import String, Long, Record
from mapear.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

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

class DicomAnonimoCreadoPayload(Record):
    id_dicom_anonimo = String()
    imagen = String()
    entorno_clinico = String()
    registro_de_diagnostico = String()
    fecha_creacion = String()
    fecha_actualizacion = String()
    contexto_procesal = String()
    notas_clinicas = String()
    data = String()

class EventoDicomAnonimoCreado(EventoIntegracion):
    data = DicomAnonimoCreadoPayload()

class EventoParquetCreado(EventoIntegracion):
    data = ParquetCreadoPayload()

class MapeoIniciadoPayload(Record):
    id_saga = String()
    paso = String()

class MapeoIniciado(EventoIntegracion):
    data = MapeoIniciadoPayload()