from pulsar.schema import String, Long, Record
from salud_tech.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)

class ComandoCrearDatasetMedicoPayload(ComandoIntegracion):
    packet_id = String()
    # TODO Cree los records para itinerarios

class ComandoCrearDatasetMedico(ComandoIntegracion):
    data = ComandoCrearDatasetMedicoPayload()