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
user_create_res = ns.model('user_req', models.UserSchema.schema_user_create_res)


@ns.route('/')
class UserAdd(Resource):
    @ns.expect(user_create_req, validate=True)
    @ns.marshal_with(user_create_res)
    @jwt_required
    @user_management_required
    def post(self):
        data = request.json
        user = services.admin.add_user(**data)
        return user
