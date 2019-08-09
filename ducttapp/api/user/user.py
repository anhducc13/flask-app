from flask_restplus import Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from . import ns

from ducttapp import models, services, repositories, extensions
from ducttapp.helpers.decorators import user_management_required

user_model = ns.model(
    name='user_res',
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

_update_user_res = ns.model(
    name="update_user_response",
    model={
        "update": fields.Boolean()
    }
)

edit_user_request_model = ns.model(
    name="edit_user_request_model",
    model={
        'fullname': fields.String(),
        'phone_number': fields.String(),
        'gender': fields.Boolean(),
        'birthday': fields.DateTime(),
        'is_active': fields.Boolean(required=True),
        'roles': fields.List(fields.Integer)
    }
)


@ns.route('/<int:user_id>')
class User(Resource):
    @jwt_required
    @user_management_required
    @ns.marshal_with(user_model)
    def get(self, user_id):
        user = services.admin.get_one_user(user_id)
        return user.to_dict()

    @jwt_required
    @user_management_required
    @ns.expect(edit_user_request_model, validate=True)
    @ns.marshal_with(_update_user_res)
    def put(self, user_id):
        current_user = repositories.user.find_one_by_id(
            user_id=get_jwt_identity()
        )
        if current_user and current_user.id == user_id:
            raise extensions.exceptions.ForbiddenException(
                message="You can't edit myself here. Please do it in profile"
            )
        data = request.json
        result = services.admin.edit_user(user_id, **data)
        return result

    @jwt_required
    @user_management_required
    def delete(self, user_id):
        current_user = repositories.user.find_one_by_id(
            user_id=get_jwt_identity()
        )
        if current_user and current_user.id == user_id:
            raise extensions.exceptions.ForbiddenException(
                message="You can't delete myself"
            )
        message = services.admin.delete_user(user_id)
        return message
