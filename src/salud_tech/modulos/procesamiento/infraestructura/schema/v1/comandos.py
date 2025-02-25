from pulsar.schema import *
from dataclasses import dataclass, field
from salud_tech.seedwork.infraestructura.schema.v1.comandos import ComandoIntegracion

class ComandoCrearDatasetPayload(ComandoIntegracion):
    id_usuario = String()
    dataset_metadata = String()

class ComandoCrearDataset(ComandoIntegracion):
    data = ComandoCrearDatasetPayload()
