from flask_restplus import Resource
from flask import request
from ducttapp import models, services
from . import ns

_forgot_pass_req = ns.model(
    'forgot_password_request', models.UserSchema.schema_forgot_password_req)


@ns.route('/forgotPassword')
class ForgotPassword(Resource):
    @ns.expect(_forgot_pass_req, validate=True)
    def post(self):
        data = request.json or request.args
        message = services.auth.forgot_pass(**data)
        return message
