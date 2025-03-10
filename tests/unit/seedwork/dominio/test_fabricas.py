import pytest
from abc import ABC, abstractmethod
from salud_tech.seedwork.dominio.fabricas import Fabrica
from salud_tech.seedwork.dominio.repositorios import Mapeador


# Implementación de prueba para la fábrica
class FabricaPrueba(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador = None) -> any:
        if mapeador:
            return mapeador.mapear(obj)
        return obj


# Implementación concreta de Mapeador
class MapeadorPrueba(Mapeador):
    def mapear(self, obj):
        return {"mapeado": obj}

    def dto_a_entidad(self, dto):
        return {"entidad": dto}

    def entidad_a_dto(self, entidad):
        return {"dto": entidad}

    def obtener_tipo(self):
        return "tipo_prueba"


def test_fabrica_es_abstracta():
    """Prueba que Fabrica no puede instanciarse directamente"""
    with pytest.raises(TypeError):
        Fabrica()


def test_fabrica_crear_objeto_sin_mapeador():
    """Prueba que FabricaPrueba crea un objeto sin mapeador"""
    fabrica = FabricaPrueba()
    objeto = {"clave": "valor"}

    resultado = fabrica.crear_objeto(objeto)

    assert resultado == objeto


def test_fabrica_crear_objeto_con_mapeador():
    """Prueba que FabricaPrueba usa un Mapeador para transformar el objeto"""
    fabrica = FabricaPrueba()
    objeto = {"clave": "valor"}
    mapeador = MapeadorPrueba()

    resultado = fabrica.crear_objeto(objeto, mapeador)

    assert resultado == {"mapeado": objeto}
