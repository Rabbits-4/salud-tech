""" Mapeadores para la capa de infraestructura del dominio de procesamiento de datos médicos

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs

"""

from salud_tech.seedwork.dominio.repositorios import Mapeador
from salud_tech.modulos.procesamiento.dominio.entidades import DatasetMedico
from salud_tech.modulos.procesamiento.dominio.objetos_valor import Metadata, RegistroDeDiagnostico, Estado
from .dto import DatasetMedicoDTO, MetadataDTO

class MapeadorDatasetMedico(Mapeador):
    
    def _procesar_metadata_dto(self, metadata_dto: MetadataDTO) -> Metadata:
        return Metadata(detalles=metadata_dto.detalles)

    def obtener_tipo(self) -> type:
        return DatasetMedico

    def entidad_a_dto(self, entidad: DatasetMedico) -> DatasetMedicoDTO:
        dataset_dto = DatasetMedicoDTO()
        dataset_dto.id = str(entidad.id)
        dataset_dto.fecha_creacion = entidad.fecha_creacion
        dataset_dto.fecha_actualizacion = entidad.fecha_actualizacion
        dataset_dto.historial_paciente_id = entidad.historial_paciente_id
        dataset_dto.contexto_procesal = entidad.contexto_procesal
        dataset_dto.notas_clinicas = entidad.notas_clinicas
        dataset_dto.estado = entidad.estado.name
        dataset_dto.registro_de_diagnostico = entidad.registro_de_diagnostico
        dataset_dto.metadata = MetadataDTO(detalles=entidad.metadata.detalles)
        return dataset_dto

    def dto_a_entidad(self, dto: DatasetMedicoDTO) -> DatasetMedico:
        dataset = DatasetMedico(
            id=dto.id,
            fecha_creacion=dto.fecha_creacion,
            fecha_actualizacion=dto.fecha_actualizacion,
            historial_paciente_id=dto.historial_paciente_id,
            contexto_procesal=dto.contexto_procesal,
            notas_clinicas=dto.notas_clinicas,
            estado=Estado(dto.estado),
            registro_de_diagnostico=dto.registro_de_diagnostico,
            metadata=self._procesar_metadata_dto(dto.metadata)
        )
        return dataset
