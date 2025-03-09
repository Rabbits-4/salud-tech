from pulsar.schema import String, Long, Record
from anonimacion.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

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

# 🔹 Payload para evento de inicio de anonimización
class AnonimacionIniciadaPayload(Record):
    id_saga = String()
    paso = String()

# 🔹 Evento de integración para indicar que el proceso de anonimización ha comenzado
class AnonimacionIniciada(EventoIntegracion):
    data = AnonimacionIniciadaPayload()