from salud_tech.seedwork.aplicacion.dto import Mapeador as AppMap
from salud_tech.seedwork.dominio.repositorios import Mapeador as RepMap

from salud_tech.modulos.procesamiento.dominio.entidades import DatasetMedico
from salud_tech.modulos.procesamiento.dominio.objetos_valor import Estado, RegistroDeDiagnostico, Metadata

from .dto import DatasetMedicoDto

from datetime import datetime


class MapeadorDatasetMedico(RepMap):

    def obtener_tipo(self) -> type:
        return DatasetMedico.__class__
    
    def dto_a_entidad(self, dto: DatasetMedicoDto) -> DatasetMedico:
        dataset = DatasetMedico()
        dataset.registro_de_diagnostico = RegistroDeDiagnostico(
            region_anatomica = dto.metadata.get('registro_de_diagnostico'),
            modalidad = dto.metadata.get('modalidad'),
            patologia = dto.metadata.get('patologia')
        )

        dataset.estado = Estado(dto.metadata.get('estado'))
        
        return dataset
    
    def entidad_a_dto(self, entidad: DatasetMedico) -> DatasetMedicoDto:
        ...

