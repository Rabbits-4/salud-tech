"""DTOs para la capa de infrastructura del dominio de procesamiento

En este archivo usted encontrará los DTOs (modelos anémicos) de
la infraestructura del dominio de procesamiento.

"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, JSON, Float, String
from salud_tech.config.db import db
from datetime import datetime
# Base = db.declarative_base() 

import uuid

class DatasetMedico(db.Model):
    __tablename__ = "datasets_medicos"
    id = Column(String, primary_key=True)
    fecha_creacion = Column(DateTime, nullable=True, default=datetime.utcnow)
    region_anatomica = Column(String, nullable=False)
    modalidad = Column(String, nullable=False)
    patologia = Column(String, nullable=False)
    entorno_clinico = Column(String, nullable=False)
    notas_clinicas = Column(String, nullable=False)
    historial_paciente_id = Column(String, nullable=False)
    condiciones_previas_paciente = Column(String, nullable=False)
    tipo_contexto_procesal = Column(String, nullable=False)
    estado = Column(String, nullable=False)
