from flask_restplus import Namespace, Resource, fields
from flask import request, jsonify

from ducttapp import models, services

ns = Namespace('auth', description='Auth operators')

_signup_request_req = ns.model(
    'signup_request_request', models.SignupSchema.signup_request_req)
_signup_request_res = ns.model(
    'signup_request_response', models.SignupSchema.signup_request_res)
_verify_res = ns.model('verify_message', model={
    'message': fields.String(required=True, description='verify success or not'),
})

_login_req = ns.model(
    'login_request', model={
        'username': fields.String(required=True, description='user name login'),
        'password': fields.String(required=True, description='password login'),
    }
)


@ns.route('/register')
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
        message = services.auth.verify(token)
        return message


@ns.route('/login')
class Login(Resource):
    @ns.expect(_login_req, validate=True)
    def post(self):
        data = request.json or request.args
        result = services.auth.login(**data)
        return result

