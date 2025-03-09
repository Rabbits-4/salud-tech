import os

from flask import Flask, jsonify, request
from flask_swagger import swagger

# Identifica el directorio base
basedir = os.path.abspath(os.path.dirname(__file__))

def registrar_handlers():
    # Importa los handlers
    import anonimacion.modulos.anonimacion.aplicacion

def importar_modelos_alchemy():
    # Import SQLAlchemy models
    import anonimacion.modulos.anonimacion.infraestructura.dto

def comenzar_consumidor():
    """
    Este es un código de ejemplo. Aunque esto sea funcional puede ser un poco peligroso tener 
    threads corriendo por si solos. Mi sugerencia es en estos casos usar un verdadero manejador
    de procesos y threads como Celery.
    """

    import threading
    import anonimacion.modulos.anonimacion.infraestructura.consumidores as anonimacion

    # Suscripción a eventos
    threading.Thread(target=anonimacion.suscribirse_a_eventos).start()

    # Suscripción a comandos
    threading.Thread(target=anonimacion.suscribirse_a_comandos).start()

def create_app(configuracion={}):
    # Init la aplicacion de Flask
    app = Flask(__name__, instance_relative_config=True)
    
    db_user = os.getenv('POSTGRES_USER', 'postgres')
    db_password = os.getenv('POSTGRES_PASSWORD', 'anonimacion_123')
    db_name = os.getenv('POSTGRES_DB', 'rabbit_anonimacion')
    db_host = os.getenv('POSTGRES_HOST', 'anonimacion_db')
    
    app.config['SQLALCHEMY_DATABASE_URI'] =\
            f'postgresql://{db_user}:{db_password}@{db_host}/{db_name}'

    app.secret_key = '9d58f98f-3ae8-4149-a09f-3a8c2012e32c'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['TESTING'] = configuracion.get('TESTING')

     # Inicializa la DB
    from anonimacion.config.db import init_db, db
    init_db(app)
     
    with app.app_context():
        importar_modelos_alchemy()
        db.create_all()
        if not app.config.get('TESTING'):
            comenzar_consumidor()

    registrar_handlers()

     # Importa Blueprints
    from . import anonimacion

    # Registro de Blueprints
    app.register_blueprint(anonimacion.bp)

    @app.route("/spec")
    def spec():
        swag = swagger(app)
        swag['info']['version'] = "1.0"
        swag['info']['title'] = "Salud Tech - Anonimacion API"
        return jsonify(swag)

    @app.route("/health")
    def health():
        return {"status": "up"}

    return app
