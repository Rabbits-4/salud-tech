import pytest
from salud_tech.seedwork.dominio.mixins import ValidarReglasMixin
from salud_tech.seedwork.dominio.reglas import ReglaNegocio
from salud_tech.seedwork.dominio.excepciones import ReglaNegocioExcepcion


# Implementación de prueba que usa la mixin
class ClasePrueba(ValidarReglasMixin):
    def __init__(self):
        pass


# Reglas de negocio de prueba
class ReglaValida(ReglaNegocio):
    def es_valido(self) -> bool:
        return True

    def __str__(self):
        return "Regla válida"


class ReglaInvalida(ReglaNegocio):
    def es_valido(self) -> bool:
        return False

    def __str__(self):
        return "Regla inválida"


def test_validar_regla_valida():
    """Prueba que no se lanza excepción si la regla es válida"""
    obj = ClasePrueba()
    regla = ReglaValida(mensaje="Regla válida")

    # No debe lanzar excepción
    obj.validar_regla(regla)


def test_validar_regla_invalida():
    """Prueba que se lanza ReglaNegocioExcepcion si la regla es inválida"""
    obj = ClasePrueba()
    regla = ReglaInvalida(mensaje="Regla inválida")

    with pytest.raises(ReglaNegocioExcepcion) as exc:
        obj.validar_regla(regla)

    assert str(exc.value) == "Regla inválida"
