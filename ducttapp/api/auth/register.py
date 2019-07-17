from flask_restplus import Resource
from flask import request
from ducttapp import models, services
from . import ns

_signup_request_req = ns.model(
    'signup_request_request', models.SignupSchema.signup_request_req)


@ns.route('/register')
class Register(Resource):
    @ns.expect(_signup_request_req, validate=True)
    def post(self):
        data = request.json or request.args
        user = services.auth.register(**data)
        return user
