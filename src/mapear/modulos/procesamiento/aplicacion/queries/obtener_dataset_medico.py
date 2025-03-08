from mapear.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from mapear.seedwork.aplicacion.queries import ejecutar_query as query
from mapear.modulos.procesamiento.infraestructura.repositorios import RepositorioDatasetMedico
from dataclasses import dataclass
from .base import QueryBaseHandler
import uuid

@dataclass
class ObtenerDatasetMedico(Query):
    id: str

class ObtenerDatasetMedicoHandler(QueryBaseHandler):

    def handle(self, query: ObtenerDatasetMedico) -> QueryResultado:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioDatasetMedico.__class__)
        dataset_medico = self.fabrica_procesamiento.crear_objeto(repositorio.obtener_por_id(query.id))
        return QueryResultado(resultado=dataset_medico)

@query.register(ObtenerDatasetMedico)
def ejecutar_query_obtener_dataset_medico(query: ObtenerDatasetMedico):
    handler = ObtenerDatasetMedicoHandler()
    return handler.handle(query)