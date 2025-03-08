import os

from flask import Flask, jsonify, request
from flask_swagger import swagger
from mapear.modulos.mapear.aplicacion.servicios import ServicioParquet
from mapear.modulos.mapear.aplicacion.dto import ParquetDto
from mapear.modulos.mapear.dominio.entidades import ParquetFile


# Identifica el directorio base
basedir = os.path.abspath(os.path.dirname(__file__))

def registrar_handlers():
    # Importa los handlers
    import mapear.modulos.mapear.aplicacion

def importar_modelos_alchemy():
    # Import SQLAlchemy models
    import mapear.modulos.mapear.infraestructura.dto

def comenzar_consumidor():
    """
    Este es un código de ejemplo. Aunque esto sea funcional puede ser un poco peligroso tener 
    threads corriendo por si solos. Mi sugerencia es en estos casos usar un verdadero manejador
    de procesos y threads como Celery.
    """

    import threading
    import mapear.modulos.mapear.infraestructura.consumidores as mapear

    # Suscripción a eventos
    threading.Thread(target=mapear.suscribirse_a_eventos).start()

    # Suscripción a comandos
    threading.Thread(target=mapear.suscribirse_a_comandos).start()

def create_app(configuracion={}):
    # Init la aplicacion de Flask
    app = Flask(__name__, instance_relative_config=True)
    
    db_user = os.getenv('POSTGRES_USER', 'mapear')
    db_password = os.getenv('POSTGRES_PASSWORD', 'mapear_123')
    db_name = os.getenv('POSTGRES_DB', 'rabbit_mapear')
    db_host = os.getenv('POSTGRES_HOST', 'mapear_db')
    
    app.config['SQLALCHEMY_DATABASE_URI'] =\
            f'postgresql://{db_user}:{db_password}@{db_host}/{db_name}'

    app.secret_key = '9d58f98f-3ae8-4149-a09f-3a8c2012e32c'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['TESTING'] = configuracion.get('TESTING')

     # Inicializa la DB
    from mapear.config.db import init_db, db
    init_db(app)
     
    with app.app_context():
        db.create_all()
        if not app.config.get('TESTING'):
            comenzar_consumidor()

    print(db, "db despues de inicializar db")
    importar_modelos_alchemy()
    registrar_handlers()

     # Importa Blueprints
    from . import mapear

    # Registro de Blueprints
    app.register_blueprint(mapear.bp)

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
