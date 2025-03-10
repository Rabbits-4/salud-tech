import pytest
from salud_tech.seedwork.dominio.excepciones import (
    ExcepcionDominio,
    IdDebeSerInmutableExcepcion,
    ReglaNegocioExcepcion,
    ExcepcionFabrica
)
from salud_tech.seedwork.dominio.reglas import ReglaNegocio


def test_excepcion_dominio():
    """Prueba que ExcepcionDominio sea una subclase de Exception"""
    assert issubclass(ExcepcionDominio, Exception)


def test_id_debe_ser_inmutable_excepcion():
    """Prueba la inicialización y mensaje de IdDebeSerInmutableExcepcion"""
    with pytest.raises(IdDebeSerInmutableExcepcion) as exc:
        raise IdDebeSerInmutableExcepcion()

    assert str(exc.value) == "El identificador debe ser inmutable"


def test_regla_negocio_excepcion():
    """Prueba la inicialización y mensaje de ReglaNegocioExcepcion"""
    
    class ReglaPrueba(ReglaNegocio):
        def es_valido(self):
            return False

        def __str__(self):
            return "Regla de negocio no cumplida"

    regla = ReglaPrueba(mensaje="La regla de negocio es invalida")

    with pytest.raises(ReglaNegocioExcepcion) as exc:
        raise ReglaNegocioExcepcion(regla)

    assert str(exc.value) == "Regla de negocio no cumplida"


def test_excepcion_fabrica():
    """Prueba la inicialización y mensaje de ExcepcionFabrica"""
    with pytest.raises(ExcepcionFabrica) as exc:
        raise ExcepcionFabrica("Error en la fábrica de objetos")

    assert str(exc.value) == "Error en la fábrica de objetos"
