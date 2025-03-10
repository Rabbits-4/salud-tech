import pytest
from salud_tech.seedwork.dominio.servicios import Servicio
from salud_tech.seedwork.dominio.reglas import ReglaNegocio
from salud_tech.seedwork.dominio.excepciones import ReglaNegocioExcepcion


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


# Implementación de prueba de un servicio
class ServicioPrueba(Servicio):
    def ejecutar(self):
        return "Servicio ejecutado"


def test_servicio_instanciacion():
    """Prueba que un servicio puede ser instanciado correctamente"""
    servicio = ServicioPrueba()
    assert isinstance(servicio, Servicio)


def test_servicio_validar_regla_valida():
    """Prueba que validar_regla no lanza excepción si la regla es válida"""
    servicio = ServicioPrueba()
    regla = ReglaValida(mensaje="Regla válida")

    # No debe lanzar excepción
    servicio.validar_regla(regla)


def test_servicio_validar_regla_invalida():
    """Prueba que validar_regla lanza ReglaNegocioExcepcion si la regla es inválida"""
    servicio = ServicioPrueba()
    regla = ReglaInvalida(mensaje="Regla inválida")

    with pytest.raises(ReglaNegocioExcepcion) as exc:
        servicio.validar_regla(regla)

    assert str(exc.value) == "Regla inválida"
