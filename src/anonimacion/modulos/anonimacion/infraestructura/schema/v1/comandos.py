from pulsar.schema import String, Long, Record
from anonimacion.seedwork.infraestructura.schema.v1.comandos import ComandoIntegracion

class ComandoCrearDicomAnonimoPayload(Record):
    packet_id = String()
    imagen = String()
    entorno_clinico = String()
    registro_de_diagnostico = String()
    fecha_creacion = String()
    fecha_actualizacion = String()
    contexto_procesal = String()
    notas_clinicas = String()
    data = String()

class ComandoCrearDicomAnonimo(ComandoIntegracion):
    data = ComandoCrearDicomAnonimoPayload()