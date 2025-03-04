import os

from flask import Flask, jsonify, request
from flask_swagger import swagger
from salud_tech.modulos.procesamiento.aplicacion.servicios import ServicioDatasetMedico
from salud_tech.modulos.procesamiento.aplicacion.dto import ParquetDto
from salud_tech.modulos.procesamiento.dominio.entidades import DatasetMedico


# Identifica el directorio base
basedir = os.path.abspath(os.path.dirname(__file__))

def registrar_handlers():
    # Importa los handlers
    import salud_tech.modulos.procesamiento.aplicacion

def importar_modelos_alchemy():
    # Import SQLAlchemy models
    import salud_tech.modulos.procesamiento.infraestructura.dto

def comenzar_consumidor():
    """
    Este es un código de ejemplo. Aunque esto sea funcional puede ser un poco peligroso tener 
    threads corriendo por si solos. Mi sugerencia es en estos casos usar un verdadero manejador
    de procesos y threads como Celery.
    """

    import threading
    import salud_tech.modulos.procesamiento.infraestructura.consumidores as procesamiento

    # Suscripción a eventos
    threading.Thread(target=procesamiento.suscribirse_a_eventos).start()

    # Suscripción a comandos
    threading.Thread(target=procesamiento.suscribirse_a_comandos).start()

def create_app(configuracion={}):
    # Init la aplicacion de Flask
    app = Flask(__name__, instance_relative_config=True)
    
    db_user = os.getenv('POSTGRES_USER', 'salud_tech')
    db_password = os.getenv('POSTGRES_PASSWORD', 'salud_tech_123')
    db_name = os.getenv('POSTGRES_DB', 'rabbit_salud_tech')
    db_host = os.getenv('POSTGRES_HOST', 'salud_tech_db')
    
    app.config['SQLALCHEMY_DATABASE_URI'] =\
            f'postgresql://{db_user}:{db_password}@{db_host}/{db_name}'

    app.secret_key = '9d58f98f-3ae8-4149-a09f-3a8c2012e32c'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['TESTING'] = configuracion.get('TESTING')

     # Inicializa la DB
    from salud_tech.config.db import init_db, db
    init_db(app)
     
    with app.app_context():
        db.create_all()
        if not app.config.get('TESTING'):
            comenzar_consumidor()

    print(db, "db despues de inicializar db")
    importar_modelos_alchemy()
    registrar_handlers()

     # Importa Blueprints
    from . import procesamiento

    # Registro de Blueprints
    app.register_blueprint(procesamiento.bp)

    @app.route("/spec")
    def spec():
        swag = swagger(app)
        swag['info']['version'] = "1.0"
        swag['info']['title'] = "Salud Tech - Procesamiento API"
        return jsonify(swag)

    @app.route("/health")
    def health():
        return {"status": "up"}

    return app
