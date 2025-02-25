""" Repositorios para el manejo de persistencia de objetos de dominio en la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará las diferentes repositorios para
persistir objetos dominio (agregaciones) en la capa de infraestructura del dominio de vuelos

"""

from aeroalpes.config.db import db
from aeroalpes.modulos.vuelos.dominio.repositorios import RepositorioReservas, RepositorioProveedores
from aeroalpes.modulos.vuelos.dominio.objetos_valor import NombreAero, Odo, Leg, Segmento, Itinerario, CodigoIATA
from aeroalpes.modulos.vuelos.dominio.entidades import Proveedor, Aeropuerto, Reserva

from salud_tech.modulos.procesamiento.dominio.fabricas import FabricaProcesamiento
from salud_tech.modulos.procesamiento.dominio.entidades import DatasetMedico
from salud_tech.modulos.procesamiento.dominio.objetos_valor import Estado, RegistroDeDiagnostico, Metadata
from salud_tech.modulos.procesamiento.dominio.repositorios import RepositorioDatasetMedico

from aeroalpes.modulos.vuelos.dominio.fabricas import FabricaVuelos
from .dto import DatasetMedico as DatasetMedicoDTO
from .mapeadores import MapeadorDatasetMedico
from uuid import UUID

class RepositorioDatasetMedicoPostgress(RepositorioDatasetMedico):

    def __init__(self):
        self._fabrica_procesamiento: FabricaProcesamiento = FabricaProcesamiento()

    @property
    def fabrica_procesamiento(self):
        return self._fabrica_procesamiento

    def obtener_por_id(self, id: UUID) -> DatasetMedico:
        dataset_medico_dto = db.session.query(DatasetMedicoDTO).filter_by(id=str(id)).one()
        return self.fabrica_procesamiento.crear_objeto(dataset_medico_dto, MapeadorDatasetMedico())

    def obtener_todos(self) -> list[Reserva]:
        # TODO
        raise NotImplementedError

    def agregar(self, reserva: Reserva):
        reserva_dto = self.fabrica_vuelos.crear_objeto(reserva, MapeadorDatasetMedico())
        db.session.add(reserva_dto)

    def actualizar(self, reserva: Reserva):
        # TODO
        raise NotImplementedError

    def eliminar(self, reserva_id: UUID):
        # TODO
        raise NotImplementedError