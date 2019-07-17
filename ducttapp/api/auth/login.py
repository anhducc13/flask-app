from flask_restplus import Resource
from flask import request
from ducttapp import models, services
from . import ns

_login_req = ns.model(
    'login_request', models.UserSchema.schema_login_req)


@ns.route('/login')
class Login(Resource):
    @ns.expect(_login_req, validate=True)
    def post(self):
        data = request.json or request.args
        result = services.auth.login(**data)
        return result
