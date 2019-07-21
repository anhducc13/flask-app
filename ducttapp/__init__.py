from flask import Flask, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import re

jwt = JWTManager()


def _after_request(response):
    allowed_origins = [
        re.compile('https?://(.*\.)?localhost'),
        # re.compile('https?://(.*\.)?teko\.vn'),
        # re.compile('https?://(.*\.)?phongvu\.vn')
    ]

    origin = request.headers.get('Origin')
    if origin:
        for allowed_origin in allowed_origins:
            if allowed_origin.match(origin):
                response.headers['Access-Control-Allow-Origin'] = origin

    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept, Authorization'

    return response


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
    app.after_request(_after_request)
    app.config['JWT_SECRET_KEY'] = config.FLASK_APP_SECRET_KEY
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
    app.config['JWT_ERROR_MESSAGE_KEY'] = 'message'
    jwt.init_app(app)
    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return models.RevokedToken.is_jti_blacklisted(jti=jti)

    api.init_app(app)
    models.init_app(app)
    # CORS(app)
    return app


app = create_app()
