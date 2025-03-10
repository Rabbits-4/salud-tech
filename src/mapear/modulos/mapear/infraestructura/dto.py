"""DTOs para la capa de infrastructura del dominio de procesamiento

En este archivo usted encontrará los DTOs (modelos anémicos) de
la infraestructura del dominio de procesamiento.

"""

from sqlalchemy import Column, DateTime, JSON, String
from mapear.config.db import db
from datetime import datetime

import uuid

class Parquet(db.Model):
    __tablename__ = "parquets"
    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    fecha_creacion = Column(DateTime, nullable=True, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, nullable=True, default=datetime.utcnow)
    historial_paciente_id = Column(String, nullable=True, default="")
    contexto_procesal = Column(String, nullable=True, default="")
    registro_de_diagnostico = Column(JSON, nullable=True, default={})
    entorno_clinico = Column(String, nullable=True, default="")
    notas_clinicas = Column(String, nullable=True, default="")  
    data = Column(JSON, nullable=True, default={})
    estado = Column(String, nullable=True, default="En Proceso")
