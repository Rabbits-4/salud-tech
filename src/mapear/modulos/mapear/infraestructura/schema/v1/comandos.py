from pulsar.schema import String, Long, Record
from mapear.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)

class ComandoCrearParquetPayload(ComandoIntegracion):
    packet_id = String()
    # TODO Cree los records para itinerarios

class ComandoCrearParquet(ComandoIntegracion):
    data = ComandoCrearParquetPayload()