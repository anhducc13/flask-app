from flask import Flask
def create_app():
    import config
    import os
    from . import api, models

    def load_app_config(app):
        app.config.from_object(config)
        app.config.from_pyfile('config.py', silent=True)

    app = Flask(
        __name__,
        instance_relative_config=True,
        instance_path=os.path.join(config.ROOT_DIR, 'instance')
    )
    app.secret_key = config.FLASK_APP_SECRET_KEY
    load_app_config(app)
    api.init_app(app)
    models.init_app(app)
    return app

app = create_app()
