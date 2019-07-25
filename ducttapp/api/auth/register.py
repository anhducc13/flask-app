from flask_restplus import Resource
from flask import request
from ducttapp import models, services
from . import ns

_signup_request_req = ns.model(
    'signup_request_request', models.SignupSchema.signup_request_req)

_signup_request_res = ns.model(
    'signup_request_response', models.SignupSchema.signup_request_res)


@ns.route('/register')
class Register(Resource):
    @ns.expect(_signup_request_req, validate=True)
    @ns.marshal_with(_signup_request_res)
    def post(self):
        data = request.json or request.args
        user = services.auth.register(**data)
        return user


@ns.route('/verifyRegister/<string:token>', endpoint='verify')
class Verify(Resource):
    def get(self, token):
        message = services.auth.verify(token)
        return message

