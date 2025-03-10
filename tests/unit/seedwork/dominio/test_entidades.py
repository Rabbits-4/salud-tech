import pytest
import uuid
from datetime import datetime
from salud_tech.seedwork.dominio.entidades import Entidad, AgregacionRaiz, Locacion
from salud_tech.seedwork.dominio.eventos import EventoDominio
from salud_tech.seedwork.dominio.excepciones import IdDebeSerInmutableExcepcion

def test_creacion_entidad():
    """Prueba la creación de una entidad con UUID y fechas automáticas"""
    entidad = Entidad(id=uuid.uuid4())

    assert isinstance(entidad.id, uuid.UUID)
    assert isinstance(entidad.fecha_creacion, datetime)
    assert isinstance(entidad.fecha_actualizacion, datetime)

def test_id_inmutable():
    """Prueba que el ID de una entidad no se puede modificar"""
    entidad = Entidad(id=uuid.uuid4())

    with pytest.raises(IdDebeSerInmutableExcepcion):
        entidad.id = uuid.uuid4()

def test_creacion_agregacion_raiz():
    """Prueba la creación de una agregación raíz con eventos"""
    agregacion = AgregacionRaiz(id=uuid.uuid4())

    assert isinstance(agregacion.id, uuid.UUID)
    assert isinstance(agregacion.eventos, list)
    assert len(agregacion.eventos) == 0

def test_agregar_evento():
    """Prueba agregar un evento a una agregación raíz"""
    agregacion = AgregacionRaiz(id=uuid.uuid4())
    evento = EventoDominio()  # Asegúrate de importar la clase correcta

    agregacion.agregar_evento(evento)

    assert len(agregacion.eventos) == 1
    assert agregacion.eventos[0] is evento

def test_limpiar_eventos():
    """Prueba limpiar eventos de una agregación raíz"""
    agregacion = AgregacionRaiz(id=uuid.uuid4())
    evento = EventoDominio()

    agregacion.agregar_evento(evento)
    assert len(agregacion.eventos) == 1

    agregacion.limpiar_eventos()
    assert len(agregacion.eventos) == 0

def test_locacion_str():
    """Prueba el método __str__ de Locacion (si es necesario)"""
    locacion = Locacion(id=uuid.uuid4())

    assert locacion is not None  