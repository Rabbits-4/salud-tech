"""DTOs para la capa de infraestructura del dominio de procesamiento de datos médicos

En este archivo usted encontrará los DTOs (modelos anémicos) de
la infraestructura del dominio de procesamiento de datos médicos

"""

from salud_tech.config.db import db
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import uuid

class DatasetMedicoDTO(db.Model):
    __tablename__ = "dataset_medico"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    fecha_creacion = Column(DateTime, nullable=False)
    fecha_actualizacion = Column(DateTime, nullable=False)
    historial_paciente_id = Column(String, nullable=False)
    contexto_procesal = Column(String, nullable=False)
    notas_clinicas = Column(String, nullable=False)
    estado = Column(String, nullable=False)
    registro_de_diagnostico = Column(String, nullable=False)
    metadata_id = Column(String, ForeignKey("metadata.id"))
    metadata = relationship("MetadataDTO", backref="dataset_medico")

class MetadataDTO(db.Model):
    __tablename__ = "metadata"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    detalles = Column(String, nullable=False)