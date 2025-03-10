import pytest
import json
from mapear.api.__init__ import create_app  # Importamos la aplicación Flask sin modificarla
from mapear.seedwork.dominio.excepciones import ExcepcionDominio


@pytest.fixture
def client(mocker):
    """Crea un cliente de pruebas con la aplicación Flask y mocks necesarios"""
    # Mockear la base de datos para que no se conecte en las pruebas
    mocker.patch('mapear.config.db.init_db', return_value=None)
    mocker.patch('mapear.config.db.db.create_all', return_value=None)

    # Mockear los consumidores para que no se inicien en pruebas
    #mocker.patch('mapear.modulos.mapear.infraestructura.consumidores.suscribirse_a_eventos', return_value=None)
    #mocker.patch('mapear.modulos.mapear.infraestructura.consumidores.suscribirse_a_comandos', return_value=None)

    app = create_app({"TESTING": True})  # Creamos la app sin conexión real
    client = app.test_client()
    yield client


def test_get_test_mapear(client):
    """Prueba el endpoint GET /test_mapear"""
    response = client.get('/mapear/test_mapear')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["message"] == "Get request processed succesfully"
