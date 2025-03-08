from pulsar.schema import String, Long, Record
from mapear.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

class ParquetCreadoPayload(Record):
    id_dicom_anonimo = String()
    imagen = String()
    entorno_clinico = String()
    registro_de_diagnostico = String()
    fecha_creacion = String()
    fecha_actualizacion = String()
    contexto_procesal = String()
    notas_clinicas = String()
    data = String()

    

class EventoParquetCreado(EventoIntegracion):
    data = ParquetCreadoPayload()