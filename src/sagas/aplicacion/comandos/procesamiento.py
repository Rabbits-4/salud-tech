from pulsar.schema import Record, String
import uuid

class RollbackProcesamiento(Record):
    id_evento = String(default=str(uuid.uuid4()))
    mensaje = String(default="Rollback en procesamiento ejecutado")