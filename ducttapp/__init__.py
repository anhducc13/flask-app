from flask import Flask
from flask_cors import CORS


def create_app():
    import config
    import os
    from . import api, models, extensions, services

    def load_app_config(app):
        app.config.from_object(config)
        app.config.from_pyfile('config.py', silent=True)

    app = Flask(
        __name__,
        instance_relative_config=True,
        instance_path=os.path.join(config.ROOT_DIR, 'instance')
    )
    CORS(app)

    load_app_config(app)
    app.config['JWT_SECRET_KEY'] = config.FLASK_APP_SECRET_KEY
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
    app.config['JWT_ERROR_MESSAGE_KEY'] = 'message'
    api.init_app(app)
    models.init_app(app)
    return app


app = create_app()
