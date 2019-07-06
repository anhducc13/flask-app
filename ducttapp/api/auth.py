from flask_restplus import Namespace, Resource, fields
from flask import request, jsonify

from ducttapp import models, services, extensions

ns = Namespace('auth', description='Auth operators')
parser = ns.parser()
parser.add_argument(
    'Authorization',
    type=str,
    help='Bearer Access Token',
    location='headers',
    required=True
)

_signup_request_req = ns.model(
    'signup_request_request', models.SignupSchema.signup_request_req)

_signup_request_res = ns.model(
    'signup_request_response', models.SignupSchema.signup_request_res)

_login_req = ns.model(
    'login_request', model={
        'username': fields.String(required=True, description='user name login'),
        'password': fields.String(required=True, description='password login'),
    }
)

_login_res = ns.model(
    'login_response', model={
        'username': fields.String(required=True, description='user name login'),
        'access_token': fields.String(required=True, description='access token login'),
        'time_expired': fields.Float(required=True, description='time expired login session')
    }
)

_reset_pass_req = ns.model(
    'reset_password_request', model={
        'old_password': fields.String(required=True, description='old password'),
        'new_password': fields.String(required=True, description='new password'),
    }
)

_forgot_pass_req = ns.model(
    'forgor_password_request', model={
        'username': fields.String(required=True, description='username'),
        'email': fields.String(required=True, description='email'),
    }
)

_forgot_pass_res = ns.model(
    'forgor_password_response', model={
        'message': fields.String(required=True, description='message'),
    }
)


@ns.route('/register')
class Register(Resource):
    @ns.expect(_signup_request_req, validate=True)
    @ns.marshal_with(_signup_request_res)
    def post(self):
        data = request.json or request.args
        user = services.auth.register(**data)
        return user


@ns.route('/verify/<string:token>', endpoint='verify')
class Verify(Resource):
    def get(self, token):
        message = services.auth.verify(token)
        return message


@ns.route('/login')
class Login(Resource):
    @ns.expect(_login_req, validate=True)
    @ns.marshal_with(_login_res)
    def post(self):
        data = request.json or request.args
        user = services.auth.login(**data)
        return user


@ns.route('/logout')
class Logout(Resource):
    @ns.expect(parser)
    def get(self):
        auth_header = request.headers.get('Authorization')
        message = services.auth.logout(auth_header)
        return message


@ns.route('/reset-password')
class ResetPassword(Resource):
    @ns.doc(body=_reset_pass_req, parser=parser)
    def post(self):
        auth_header = request.headers.get('Authorization')
        two_pass = request.json or request.args
        message = services.auth.reset_pass(
            auth_header,
            two_pass['old_password'],
            two_pass['new_password']
        )
        return message


@ns.route('/forgot-password')
class ForgotPassword(Resource):
    @ns.expect(_forgot_pass_req, validate=True)
    @ns.marshal_with(_forgot_pass_res)
    def post(self):
        data = request.json or request.args
        message = services.auth.forgot_pass(**data)
        return message