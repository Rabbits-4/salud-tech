import os

from flask import Flask, jsonify, request
from flask_swagger import swagger
import threading

from salud_tech.config.db import init_db, db
from salud_tech.modulos.procesamiento.aplicacion.servicios import ServicioDatasetMedico
from salud_tech.modulos.procesamiento.aplicacion.dto import DatasetMedicoDto
from salud_tech.modulos.procesamiento.infraestructura.consumidores import suscribirse_a_eventos, suscribirse_a_comandos
from salud_tech.modulos.procesamiento.infraestructura.dto import *

# Identifica el directorio base
basedir = os.path.abspath(os.path.dirname(__file__))

def registrar_handlers():
    import salud_tech.modulos.procesamiento.aplicacion

def importar_modelos_alchemy():
    import salud_tech.modulos.procesamiento.infraestructura.dto

def comenzar_consumidor():
    threading.Thread(target=suscribirse_a_eventos).start()
    threading.Thread(target=suscribirse_a_comandos).start()

def create_app(configuracion={}):
    app = Flask(__name__, instance_relative_config=True)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = os.getenv('SECRET_KEY', 'default-secret-key')
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['TESTING'] = configuracion.get('TESTING', False)

    init_db(app)
    importar_modelos_alchemy()
    registrar_handlers()

    with app.app_context():
        db.create_all()
        if not app.config.get('TESTING'):
            comenzar_consumidor()

    from . import procesamiento
    app.register_blueprint(procesamiento.bp)

    @app.route("/spec")
    def spec():
        swag = swagger(app)
        swag['info']['version'] = "1.0"
        swag['info']['title'] = "My API"
        return jsonify(swag)

    @app.route("/health")
    def health():
        return {"status": "up"}
    
    @app.route("/procesamiento/procesar-dataset", methods=['POST'])
    def procesar_dataset():
        datos = request.get_json()
        dataset_dto = DatasetMedicoDto(
            packet_id=datos.get('packet_id'),
            entorno_clinico=datos.get('entorno_clinico'),
            metadata=datos.get('metadata'),
            data=datos.get('data')
        )
        servicio = ServicioDatasetMedico()
        resultado = servicio.crear_dataset_medico(dataset_dto)
        return jsonify({"mensaje": "Dataset procesado exitosamente", "id": resultado.packet_id}), 201

    return app
