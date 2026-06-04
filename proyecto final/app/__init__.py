from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Configuracion')
    
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith('mysql'):
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            'connect_args': {
                'ssl': {
                    'ssl_mode': 'REQUIRED'
                }
            }
        }

    db.init_app(app)
    
    with app.app_context():
        # Import all models so SQLAlchemy create_all() sees every table metadata
        from app.models.usuario import Usuario
        from app.models.turno import Turno
        from app.models.grupo import Grupo
        from app.models.materia import Materia
        from app.models.docente import Docente
        from app.models.alumno import Alumno
        from app.models.planeacion import Planeacion
        from app.models.calificacion import Calificacion

        # Import and register blueprints
        from app.routes.auth import bp as auth_bp
        from app.routes.dashboard import bp as dashboard_bp
        from app.routes.alumnos import bp as alumnos_bp
        from app.routes.grupos import bp as grupos_bp
        from app.routes.materias import bp as materias_bp
        from app.routes.docentes import bp as docentes_bp
        from app.routes.planeacion import bp as planeacion_bp
        from app.routes.calificaciones import bp as calificaciones_bp
        
        app.register_blueprint(auth_bp)
        app.register_blueprint(dashboard_bp)
        app.register_blueprint(alumnos_bp)
        app.register_blueprint(grupos_bp)
        app.register_blueprint(materias_bp)
        app.register_blueprint(docentes_bp)
        app.register_blueprint(planeacion_bp)
        app.register_blueprint(calificaciones_bp)
        
        db.create_all()
    
    return app
