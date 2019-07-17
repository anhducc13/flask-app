from flask_restplus import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ducttapp import models, services
from . import ns


_update_pass_req = ns.model(
    'update_pass_request', models.UserSchema.schema_update_password_req)


@ns.route('/updatePassword')
class UpdatePassword(Resource):
    @ns.expect(_update_pass_req, validate=True)
    @jwt_required
    def post(self):
        username = get_jwt_identity()
        two_pass = request.json or request.args
        message = services.auth.update_pass(
            username,
            two_pass['old_password'],
            two_pass['new_password']
        )
        return message
