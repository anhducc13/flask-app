from flask_restplus import Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from ducttapp import models, services
from . import ns

edit_profile_request_model = ns.model(
    name="edit_profile_request_model",
    model={
        'username': fields.String(required=True),
        'fullname': fields.String(),
        'phone_number': fields.String(),
        'gender': fields.Boolean(),
        'birthday': fields.DateTime(),
        'avatar': fields.String()
    }
)

edit_profile_model = ns.model(
    name='edit_profile_model',
    model={
        'id': fields.Integer(),
        'email': fields.String(),
        'username': fields.String(),
        'is_admin': fields.Boolean(),
        'is_active': fields.Boolean(),
        'updated_at': fields.DateTime(),
        'fullname': fields.String(),
        'phone_number': fields.String(),
        'gender': fields.Boolean(),
        'birthday': fields.DateTime(),
        'avatar': fields.String(),
        'roles': fields.List(fields.Integer())
    }
)


@ns.route('/editProfile')
class EditProfile(Resource):
    @jwt_required
    @ns.expect(edit_profile_request_model)
    @ns.marshal_with(edit_profile_model)
    def post(self):
        user_id = get_jwt_identity()
        data = request.json
        user = services.auth.edit_profile_user(
            user_id=user_id,
            **data
        )
        return user.to_dict()
