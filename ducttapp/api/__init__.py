from flask import Blueprint
from flask_restplus import Api
from .auth import ns as auth_ns

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
    api.add_namespace(auth_ns)
    app.register_blueprint(api_bp)