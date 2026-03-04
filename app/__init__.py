from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'

@login.unauthorized_handler
def unauthorized():
    from flask import request, jsonify, redirect, url_for
    if request.blueprint == 'api' or request.path.startswith('/api/'):
        return jsonify({'error': 'Unauthorized', 'message': 'Session expired or not logged in'}), 401
    return redirect(url_for(login.login_view, next=request.url))

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    # Register blueprints (will be created later)
    # Register blueprints (will be created later)
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    @app.before_request
    def update_last_seen():
        from flask_login import current_user
        if current_user.is_authenticated:
            from datetime import datetime
            current_user.last_seen = datetime.utcnow()
            db.session.commit()

    return app

from app import models
