from anonimizar.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from anonimizar.seedwork.aplicacion.queries import ejecutar_query as query
from anonimizar.modulos.procesamiento.infraestructura.repositorios import RepositorioDicomAnonimo
from dataclasses import dataclass
from .base import QueryBaseHandler
import uuid

@dataclass
class ObtenerDicomAnonimo(Query):
    id: str

class ObtenerDicomAnonimoHandler(QueryBaseHandler):

    def handle(self, query: ObtenerDicomAnonimo) -> QueryResultado:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioDicomAnonimo.__class__)
        dicom_anonimo = repositorio.obtener_por_id(query.id)
        return QueryResultado(resultado=dicom_anonimo)

@query.register(ObtenerDicomAnonimo)
def ejecutar_query_obtener_dicom_anonimo(query: ObtenerDicomAnonimo):
    handler = ObtenerDicomAnonimoHandler()
    return handler.handle(query)