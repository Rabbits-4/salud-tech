""" Mapeadores para la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs

"""

from mapear.seedwork.dominio.repositorios import Mapeador
from mapear.modulos.procesamiento.dominio.objetos_valor import RegionAnatomica, Modalidad, Patologia, EntornoClinico, NotasClinicas, HistorialPaciente, ContextoProcesal, Imagen, Metadata, RegistroDeDiagnostico
from mapear.modulos.procesamiento.dominio.entidades import DatasetMedico
from .dto import DatasetMedico as DatasetMedicoDTO

class MapeadorDatasetMedico(Mapeador):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def obtener_tipo(self) -> type:
        return DatasetMedico.__class__

    def entidad_a_dto(self, entidad: DatasetMedico) -> DatasetMedicoDTO:
        id = str(entidad.id)
        region_anatomica= entidad.registro_de_diagnostico.region_anatomica
        modalidad = entidad.registro_de_diagnostico.modalidad
        patologia = entidad.registro_de_diagnostico.patologia
        entorno_clinico = "entidad.metadata.entorno_clinico"
        notas_clinicas = "entidad.metadata.notas_clinicas"
        historial_paciente_id = "entidad.metadata.historial_paciente"
        condiciones_previas_paciente = "jum"
        tipo_contexto_procesal = "entidad.metadata.contexto_procesal"


        dataset_medico_dto = DatasetMedicoDTO(
            id=id,
            region_anatomica=region_anatomica,
            modalidad=modalidad,
            patologia=patologia,
            entorno_clinico=entorno_clinico,
            notas_clinicas=notas_clinicas,
            historial_paciente_id=historial_paciente_id,
            condiciones_previas_paciente=condiciones_previas_paciente,
            tipo_contexto_procesal=tipo_contexto_procesal,
            estado = "Finalizado"
        )

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