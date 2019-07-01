from flask_restplus import Namespace, Resource
from flask import request

from ducttapp import models, services

ns = Namespace('register', description='Sign in operators')

_signup_request_req = ns.model(
    'signup_request_req', models.SignupSchema.signup_request_req)
_signup_request_res = ns.model(
    'signup_request_res', models.SignupSchema.signup_request_res)

@ns.route('/')
class Register(Resource):
    @ns.expect(_signup_request_req, validate=True)
    @ns.marshal_with(_signup_request_res)
    def post(self):
        data = request.json or request.args
        # username = data['username']
        # email = data['email']
        # password = data['password']
        user = services.signup.create_user(**data)
        return user