from pulsar.schema import Record, String
import uuid

class DicomMapeoFallido(Record):
    id_evento = String(default=str(uuid.uuid4()))
    mensaje_error = String()
    timestamp = String()