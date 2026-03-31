"""Main Flask application entrypoint."""
import os
from datetime import datetime

from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

# Flask extensions are created globally and initialized in create_app.
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()


@login_manager.user_loader
def load_user(user_id):
    """Flask-Login callback for loading users by ID."""
    from models.user import User

    return User.query.get(int(user_id))


def create_app():
    """Application factory function."""
    app = Flask(__name__)
    app.config.from_object(Config)

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"

    # Blueprint imports are delayed to avoid circular imports.
    from routes.admin_routes import admin_bp
    from routes.analysis_routes import analysis_bp
    from routes.auth_routes import auth_bp
    from routes.chatbot_routes import chatbot_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(analysis_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(admin_bp)

    @app.context_processor
    def inject_now():
        return {"now": datetime.utcnow()}

    @app.route("/")
    def index():
        return render_template("index.html")

    return app


if __name__ == "__main__":
    application = create_app()
    application.run(debug=True)
