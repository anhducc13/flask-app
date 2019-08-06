from flask import Blueprint
from flask_restplus import Api
from .auth import ns as auth_ns
from .user import ns as user_ns
from .category import ns as category_ns
from ducttapp.extensions.exceptions import global_error_handler
from ducttapp import jwt

api_bp = Blueprint('api', __name__, url_prefix='/api')

api = Api(
    app=api_bp,
    version='1.0',
    title='Ductt API',
    validate=False,
    # doc='' # disable Swagger UI
)


def init_app(app, **kwargs):
    """
    :param flask.Flask app: the app
    :param kwargs:
    :return:
    """
    jwt._set_error_handler_callbacks(api)
    api.add_namespace(auth_ns)
    api.add_namespace(user_ns)
    api.add_namespace(category_ns)
    app.register_blueprint(api_bp)
    api.error_handlers[Exception] = global_error_handler
