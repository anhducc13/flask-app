from flask_restplus import Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from . import ns

from ducttapp import models, services, repositories, extensions
from ducttapp.helpers.decorators import user_management_required

role_model = ns.model(
    name='Role',
    model=models.RoleSchema.role_res_schema
)

user_fields = models.UserSchema.schema_user_create_res.copy()
user_fields.update({
    'roles': fields.List(fields.Nested(role_model))
})

user_model = ns.model('user_res', user_fields)

_update_user_res = ns.model(
    name="update_user_response",
    model={
        "update": fields.Boolean()
    }
)


@ns.route('/<int:user_id>')
class User(Resource):
    @jwt_required
    @user_management_required
    @ns.marshal_with(user_model)
    def get(self, user_id):
        user = services.admin.get_one_user(user_id)
        return user

    @jwt_required
    @user_management_required
    @ns.marshal_with(_update_user_res)
    def put(self, user_id):
        current_user = repositories.user.find_one_by_email_or_username_in_user_ignore_case(
            username=get_jwt_identity()
        )
        if current_user and current_user.id == user_id:
            raise extensions.exceptions.ForbiddenException(
                message="You can't edit myself"
            )
        result = services.admin.edit_user(user_id, request.form)
        return result

    @jwt_required
    @user_management_required
    def delete(self, user_id):
        current_user = repositories.user.find_one_by_email_or_username_in_user_ignore_case(
            username=get_jwt_identity()
        )
        if current_user and current_user.id == user_id:
            raise extensions.exceptions.ForbiddenException(
                message="You can't delete myself"
            )
        message = services.admin.delete_user(user_id)
        return message
