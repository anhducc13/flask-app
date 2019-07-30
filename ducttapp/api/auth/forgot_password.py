from flask_restplus import Resource, fields
from flask import request
from ducttapp import models, services
from . import ns

_forgot_pass_req = ns.model(
    name='forgot_password_request',
    model={
        'username': fields.String(required=True, min_length=1),
        'email': fields.String(required=True, min_length=1)
    })

_forgot_pass_res = ns.model(
    name="forgot_password_response",
    model={
        'sendPassword': fields.Boolean(),
    })


@ns.route('/forgotPassword')
class ForgotPassword(Resource):
    @ns.expect(_forgot_pass_req, validate=True)
    @ns.marshal_with(_forgot_pass_res)
    def post(self):
        data = request.json or request.args
        message = services.auth.forgot_pass(**data)
        return message
