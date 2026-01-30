from flask import Flask
from config import config
from app.extensions import db, migrate, login_manager

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Register Blueprints
    from app.main import main_bp
    app.register_blueprint(main_bp)

    from app.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.admin import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from app.faculty import faculty_bp
    app.register_blueprint(faculty_bp, url_prefix='/faculty')

    from app.student import student_bp
    app.register_blueprint(student_bp, url_prefix='/student')

    return app
