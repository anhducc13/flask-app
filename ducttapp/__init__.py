from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

jwt = JWTManager()


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

    load_app_config(app)
    app.config['JWT_SECRET_KEY'] = config.FLASK_APP_SECRET_KEY
    # app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    # app.config['JWT_COOKIE_SECURE'] = False
    # app.config['JWT_COOKIE_CSRF_PROTECT'] = True
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
    app.config['JWT_ERROR_MESSAGE_KEY'] = 'message'
    jwt.init_app(app)
    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return models.RevokedToken.is_jti_blacklisted(jti=jti)

    models.init_app(app)
    api.init_app(app)
    CORS(app)
    return app


app = create_app()
