from salud_tech.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from salud_tech.seedwork.aplicacion.queries import ejecutar_query as query
from salud_tech.modulos.procesamiento.infraestructura.repositorios import RepositorioDatasetMedico
from dataclasses import dataclass
from .base import QueryBaseHandler
from aeroalpes.modulos.vuelos.aplicacion.mapeadores import MapeadorReserva
import uuid

@dataclass
class ObtenerDatasetMedico(Query):
    id: str

class ObtenerReservaHandler(QueryBaseHandler):

    def handle(self, query: ObtenerDatasetMedico) -> QueryResultado:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioDatasetMedico.__class__)
        reserva =  self.fabrica_vuelos.crear_objeto(repositorio.obtener_por_id(query.id), MapeadorReserva())
        return QueryResultado(resultado=reserva)

@query.register(ObtenerDatasetMedico)
def ejecutar_query_obtener_reserva(query: ObtenerDatasetMedico):
    handler = ObtenerReservaHandler()
    return handler.handle(query)