from flask_restplus import Resource, fields
from ducttapp import helpers
from flask import request
from flask_jwt_extended import jwt_required
from . import ns

from ducttapp import models, services
from ducttapp.helpers.decorators import user_management_required

user_create_req = ns.model(
    name='user_res',
    model={
        'email': fields.String(
            required=True,
            description='user email',
            pattern=helpers.validators.REGEX_EMAIL
        ),
        'username': fields.String(
            required=True,
            description='user username',
            pattern=helpers.validators.REGEX_USERNAME
        ),
        'roles': fields.List(fields.Integer)
    }
)

user_model = ns.model(
    name='user_model',
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


@ns.route('/')
class UserAdd(Resource):
    @ns.expect(user_create_req, validate=True)
    @ns.marshal_with(user_model)
    @jwt_required
    @user_management_required
    def post(self):
        data = request.json
        user = services.admin.add_user(**data)
        return user
