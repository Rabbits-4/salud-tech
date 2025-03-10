from pulsar.schema import Record, String
import uuid

class DicomAnonimizadoFallido(Record):
    id_evento = String(default=str(uuid.uuid4()))
    mensaje_error = String()
    timestamp = String()

class RollbackAnonimacionCompletado(Record):
    id_evento = String(default=str(uuid.uuid4()))
    mensaje = String(default="Rollback en anonimación completado")