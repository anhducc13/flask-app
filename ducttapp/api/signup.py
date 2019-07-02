from flask_restplus import Namespace, Resource, fields
from flask import request

from ducttapp import models, services

ns = Namespace('register', description='Sign in operators')

_signup_request_req = ns.model(
    'signup_request_req', models.SignupSchema.signup_request_req)
_signup_request_res = ns.model(
    'signup_request_res', models.SignupSchema.signup_request_res)
_verify_res = ns.model(model={
    'message': fields.String(required=True, description='verify success or not'),
})

@ns.route('/')
class Register(Resource):
    @ns.expect(_signup_request_req, validate=True)
    @ns.marshal_with(_signup_request_res)
    def post(self):
        data = request.json or request.args
        user = services.signup.create_user_to_signup_request(**data)
        return user

@ns.route('/verify/<string:token>')
class Verify(Resource):
    @ns.marshal_with(_verify_res)
    def get(self, token):
        message = services.signup.verify(token)
        return message
        