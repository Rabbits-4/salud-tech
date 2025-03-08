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
    id = Column(String, primary_key=True)
    fecha_creacion = Column(DateTime, nullable=True, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, nullable=True, default=datetime.utcnow)
    registro_de_diagnostico = Column(String, nullable=True)
    contexto_procesal = Column(String, nullable=True)
    notas_clinicas = Column(String, nullable=True)
    data = Column(JSON, nullable=True)
    estado = Column(String, nullable=True)
