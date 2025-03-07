from anonimizar.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from anonimizar.seedwork.aplicacion.queries import ejecutar_query as query
from anonimizar.modulos.procesamiento.infraestructura.repositorios import RepositorioDatasetAnonimo
from dataclasses import dataclass
from .base import QueryBaseHandler
import uuid

@dataclass
class ObtenerDatasetAnonimo(Query):
    id: str

class ObtenerDatasetAnonimoHandler(QueryBaseHandler):

    def handle(self, query: ObtenerDatasetAnonimo) -> QueryResultado:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioDatasetAnonimo.__class__)
        dataset_anonimo = self.fabrica_procesamiento.crear_objeto(repositorio.obtener_por_id(query.id))
        return QueryResultado(resultado=dataset_anonimo)

@query.register(ObtenerDatasetAnonimo)
def ejecutar_query_obtener_dataset_anonimo(query: ObtenerDatasetAnonimo):
    handler = ObtenerDatasetAnonimoHandler()
    return handler.handle(query)