"""
DTOs para la capa de infraestructura del dominio de anonimación

En este archivo usted encontrará los DTOs (modelos anémicos) de
la infraestructura del dominio de anonimación.

"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, JSON, String
from anonimacion.config.db import db
from datetime import datetime

class DicomAnonimo(db.Model):
    __tablename__ = "dicoms_anonimizados"
    
    id = Column(String, primary_key=True)
    imagen = Column(String, nullable=False)
    entorno_clinico = Column(String, nullable=False)
    registro_de_diagnostico = Column(JSON, nullable=False)
    fecha_creacion = Column(DateTime, nullable=True, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    contexto_procesal = Column(String, nullable=False)
    notas_clinicas = Column(String, nullable=True)
    data = Column(JSON, nullable=True)

class RelacionPaciente(db.Model):
    __tablename__ = "relaciones_pacientes"

    token = Column(String, primary_key=True)
    historial_paciente_id = Column(String, nullable=False)
    nombre = Column(String, nullable=False)
    direccion = Column(String, nullable=False)
    telefono = Column(String, nullable=False)