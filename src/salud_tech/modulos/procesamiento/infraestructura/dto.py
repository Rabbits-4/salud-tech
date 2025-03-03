"""DTOs para la capa de infrastructura del dominio de procesamiento

En este archivo usted encontrará los DTOs (modelos anémicos) de
la infraestructura del dominio de procesamiento.

"""

from salud_tech.config.db import db

import uuid

Base = db.declarative_base()

class DatasetMedico(db.Model):
    __tablename__ = "datasets_medicos"
    id = db.Column(db.String, primary_key=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False)
    region_anatomica = db.Column(db.String, nullable=False)
    modalidad = db.Column(db.String, nullable=False)
    patologia = db.Column(db.String, nullable=False)
    entorno_clinico = db.Column(db.String, nullable=False)
    notas_clinicas = db.Column(db.String, nullable=False)
    historial_paciente_id = db.Column(db.String, nullable=False)
    condiciones_previas_paciente = db.Column(db.String, nullable=False)
    tipo_contexto_procesal = db.Column(db.String, nullable=False)
    estado = db.Column(db.String, nullable=False)
