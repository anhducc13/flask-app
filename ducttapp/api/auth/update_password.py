from flask_restplus import Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ducttapp import models, services
from ducttapp.helpers.validators import REGEX_PASSWORD
from . import ns


_update_pass_req = ns.model(
    name='update_pass_request',
    model={
        "old_password": fields.String(required=True, min_length=1),
        "new_password": fields.String(required=True, pattern=REGEX_PASSWORD)
    })

_update_pass_res = ns.model(
    name='update_pass_response',
    model={
        "updatePassword": fields.Boolean()
    })


@ns.route('/updatePassword')
class UpdatePassword(Resource):
    @ns.expect(_update_pass_req, validate=True)
    @jwt_required
    def post(self):
        user_id = get_jwt_identity()
        two_pass = request.json or request.args
        result = services.auth.update_pass(
            user_id,
            two_pass['old_password'],
            two_pass['new_password']
        )
        return result
