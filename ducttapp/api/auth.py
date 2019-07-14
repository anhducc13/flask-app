from flask_restplus import Namespace, Resource, fields
from flask import request

from ducttapp import models, services

ns = Namespace('auth', description='Auth operators')
parser = ns.parser()

_signup_request_req = ns.model(
    'signup_request_request', models.SignupSchema.signup_request_req)

_signup_request_res = ns.model(
    'signup_request_response', models.SignupSchema.signup_request_res)

_login_req = ns.model(
    'login_request', models.UserSchema.schema_login_req)

_login_res = ns.model(
    'login_response', models.UserSchema.schema_login_res)

_update_pass_req = ns.model(
    'update_pass_request', models.UserSchema.schema_update_password_req)

_update_pass_res = ns.model(
    'update_pass_response', models.UserSchema.schema_notify_res)

_forgot_pass_req = ns.model(
    'forgot_password_request', models.UserSchema.schema_forgot_password_req)

_forgot_pass_res = ns.model(
    'forgot_password_response', models.UserSchema.schema_notify_res)

parser.add_argument(
    'Authorization',
    type=str,
    help='Bearer Access Token',
    location='headers',
    required=True
)


@ns.route('/register')
class Register(Resource):
    @ns.expect(_signup_request_req, validate=True)
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
    def post(self):
        data = request.json or request.args
        print(data)
        result = services.auth.login(**data)
        return result


@ns.route('/forgotPassword')
class ForgotPassword(Resource):
    @ns.expect(_forgot_pass_req, validate=True)
    def post(self):
        data = request.json or request.args
        message = services.auth.forgot_pass(**data)
        return message


@ns.route('/logout')
class Logout(Resource):
    @ns.doc(parser=parser)
    def get(self):
        auth_header = request.headers.get('Authorization')
        message = services.auth.logout(auth_header)
        return message


@ns.route('/updatePassword')
class UpdatePassword(Resource):
    @ns.doc(body=_update_pass_req, parser=parser)
    def post(self):
        auth_header = request.headers.get('Authorization')
        two_pass = request.json or request.args
        message = services.auth.update_pass(
            auth_header,
            two_pass['old_password'],
            two_pass['new_password']
        )
        return message



