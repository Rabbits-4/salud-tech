from mapear.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from mapear.seedwork.aplicacion.queries import ejecutar_query as query
from mapear.modulos.mapear.infraestructura.repositorios import RepositorioParquet
from mapear.modulos.mapear.aplicacion.mapeadores import MapeadorParquet
from .base import QueryBaseHandler

from dataclasses import dataclass
import uuid

@dataclass
class ObtenerParquets(Query):
    ...

class ObtenerTodosParquetsHandler(QueryBaseHandler):

    def handle(self) -> QueryResultado:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioParquet.__class__)
        raw_parquets = repositorio.obtener_todos()

        #parquets = self.fabrica_mapear.crear_objeto(raw_parquets, MapeadorParquet())
        return QueryResultado(resultado=raw_parquets)

@query.register(ObtenerParquets)
def ejecutar_query_obtener__todos_parquets(query):
    handler = ObtenerTodosParquetsHandler()
    return handler.handle()