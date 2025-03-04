from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

import salud_tech.modulos.procesamiento.dominio.objetos_valor as ov
from salud_tech.seedwork.dominio.entidades import AgregacionRaiz
from .eventos import ParcketCreado

@dataclass
class Parcket(AgregacionRaiz):
    id: str
    fecha_creacion: str
    entorno_clinico: str
    registro_de_diagnostico: str
    fecha_creacion: str 
    fecha_actualizacion: str
    historial_paciente_id: str
    contexto_procesal: str
    notas_clinicas: str
    data: dict

    def crear_dataset(self, dataset: Parcket):

        self.agregar_evento(ParcketCreado(
            id=self.id,
            fecha_creacion=self.fecha_creacion,
            entorno_clinico=self.entorno_clinico,
            registro_de_diagnostico=self.registro_de_diagnostico,
            fecha_creacion=self.fecha_creacion,
            fecha_actualizacion=self.fecha_actualizacion,
            historial_paciente_id=self.historial_paciente_id,
            contexto_procesal=self.contexto_procesal,
            notas_clinicas=self.notas_clinicas,
            data=self.data            
        ))


    

