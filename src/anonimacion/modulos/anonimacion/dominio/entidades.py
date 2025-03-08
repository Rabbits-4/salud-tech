from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

import anonimacion.modulos.anonimacion.dominio.objetos_valor as ov
from anonimacion.seedwork.dominio.entidades import AgregacionRaiz
from .eventos import DicomAnonimizado

@dataclass
class DicomAnonimo(AgregacionRaiz):
    id: str
    token: str = None
    imagen: ov.Imagen = None
    entorno_clinico: ov.EntornoClinico = None
    registro_de_diagnostico: Optional[ov.RegistroDeDiagnostico] = None
    fecha_creacion: str = None
    fecha_actualizacion: str = None
    contexto_procesal: ov.ContextoProcesal = None
    notas_clinicas: Optional[ov.NotasClinicas] = None
    data: Optional[ov.Data] = None

    def anonimizar(self):
        self.token = str(uuid.uuid4()) 

        self.agregar_evento(DicomAnonimizado(
            id=self.id,
            token=self.token,
            imagen=self.imagen,
            entorno_clinico=self.entorno_clinico,
            registro_de_diagnostico=self.registro_de_diagnostico,
            fecha_creacion=self.fecha_creacion,
            fecha_actualizacion=self.fecha_actualizacion,
            contexto_procesal=self.contexto_procesal,
            notas_clinicas=self.notas_clinicas,
            data=self.data
        ))


    

