from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from config import Config

db = SQLAlchemy()
csrf = CSRFProtect()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.secret_key = 'your_secret_key'


    db.init_app(app)
    # csrf.init_app(app)

    with app.app_context():
        from app import routes, models
        from app.forms import SearchForm

        @app.context_processor
        def inject_search_form():
            return dict(search_form=SearchForm())

        db.create_all()

    return app