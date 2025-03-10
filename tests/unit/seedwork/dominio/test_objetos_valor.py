import unittest
from datetime import datetime
import dataclasses
from salud_tech.seedwork.dominio.objetos_valor import Codigo, Pais, Ciudad  # Asegúrate de importar correctamente
from salud_tech.seedwork.dominio.entidades import Locacion  # Suponiendo que Locacion está en entidades.py

class TestObjetosValor(unittest.TestCase):

    def test_codigo(self):
        """Prueba la creación y acceso a un Código"""
        codigo = Codigo(codigo="ABC123")
        self.assertEqual(codigo.codigo, "ABC123")

        # Verificar que es inmutable
        with self.assertRaises(dataclasses.FrozenInstanceError):
            codigo.codigo = "XYZ789"

    def test_pais(self):
        """Prueba la creación y acceso a un País"""
        codigo_pais = Codigo(codigo="CO")
        pais = Pais(codigo=codigo_pais, nombre="Colombia")

        self.assertEqual(pais.codigo, codigo_pais)
        self.assertEqual(pais.nombre, "Colombia")

        # Verificar que es inmutable
        with self.assertRaises(dataclasses.FrozenInstanceError):
            pais.nombre = "Ecuador"

    def test_ciudad(self):
        """Prueba la creación y acceso a una Ciudad"""
        codigo_pais = Codigo(codigo="CO")
        pais = Pais(codigo=codigo_pais, nombre="Colombia")
        codigo_ciudad = Codigo(codigo="BOG")
        ciudad = Ciudad(pais=pais, codigo=codigo_ciudad, nombre="Bogotá")

        self.assertEqual(ciudad.pais, pais)
        self.assertEqual(ciudad.codigo, codigo_ciudad)
        self.assertEqual(ciudad.nombre, "Bogotá")

        # Verificar que es inmutable
        with self.assertRaises(dataclasses.FrozenInstanceError):
            ciudad.nombre = "Medellín"