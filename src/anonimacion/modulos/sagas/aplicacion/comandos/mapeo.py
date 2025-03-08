from pulsar.schema import Record, String
import uuid

class RollbackMapeo(Record):
    id_evento = String(default=str(uuid.uuid4()))
    mensaje = String(default="Rollback en mapeo ejecutado")