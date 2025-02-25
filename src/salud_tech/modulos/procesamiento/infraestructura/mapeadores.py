""" Mapeadores para la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs

"""

from salud_tech.seedwork.dominio.repositorios import Mapeador
from salud_tech.modulos.procesamiento.dominio.objetos_valor import RegionAnatomica, Modalidad, Patologia, EntornoClinico, NotasClinicas, HistorialPaciente, ContextoProcesal, Imagen, Metadata, RegistroDeDiagnostico
from salud_tech.modulos.procesamiento.dominio.entidades import DatasetMedico
from .dto import DatasetMedico as DatasetMedicoDTO

class MapeadorDatasetMedico(Mapeador):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def obtener_tipo(self) -> type:
        return DatasetMedico.__class__

    def entidad_a_dto(self, entidad: DatasetMedico) -> DatasetMedicoDTO:
        
        dataset_medico_dto = DatasetMedicoDTO()
        dataset_medico_dto.fecha_creacion = entidad.fecha_creacion
        dataset_medico_dto.fecha_creacion = entidad.fecha_actualizacion
        dataset_medico_dto.id = str(entidad.id)

        return dataset_medico_dto

    def dto_a_entidad(self, dto: DatasetMedicoDTO) -> DatasetMedico:
        dataset_medico = DatasetMedico(dto.id, dto.fecha_creacion, dto.fecha_actualizacion)

        region_anatomica = RegionAnatomica(dto.region_anatomica)
        modalidad = Modalidad(dto.modalidad)
        patologia = Patologia(dto.patologia)
        entorno_clinico = EntornoClinico(dto.entorno_clinico)
        notas_clinicas = NotasClinicas(dto.notas_clinicas)
        historial_paciente = HistorialPaciente(dto.historial_paciente_id)
        contexto_procesal = ContextoProcesal(dto.tipo_contexto_procesal)

        dataset_medico.registro_de_diagnostico = RegistroDeDiagnostico(
            region_anatomica=region_anatomica,
            modalidad=modalidad,
            patologia=patologia            
        )
        dataset_medico.metadata = Metadata(
            entorno_clinico=entorno_clinico,
            notas_clinicas=notas_clinicas,
            historial_paciente=historial_paciente,
            contexto_procesal=contexto_procesal,
            estado=dto.estado
        )
        
        return dataset_medico