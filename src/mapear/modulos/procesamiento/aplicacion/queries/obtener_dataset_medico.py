from mapear.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from mapear.seedwork.aplicacion.queries import ejecutar_query as query
from mapear.modulos.procesamiento.infraestructura.repositorios import RepositorioParquet
from dataclasses import dataclass
from .base import QueryBaseHandler
import uuid

@dataclass
class ObtenerParquet(Query):
    id: str

class ObtenerParquetHandler(QueryBaseHandler):

    def handle(self, query: ObtenerParquet) -> QueryResultado:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioParquet.__class__)
        parquet = self.fabrica_mapear.crear_objeto(repositorio.obtener_por_id(query.id))
        return QueryResultado(resultado=parquet)

@query.register(ObtenerParquet)
def ejecutar_query_obtener_parquet(query: ObtenerParquet):
    handler = ObtenerParquetHandler()
    return handler.handle(query)