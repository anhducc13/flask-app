from flask_restplus import Resource, fields
from flask_jwt_extended import jwt_required
from flask import request
from . import ns

from ducttapp import models, services
from ducttapp.helpers.decorators import admin_required

_user_create_res = ns.model('user_req', models.UserSchema.schema_user_create_res)

_update_user_res = ns.model(
    name="update_user_response",
    model={
        "update": fields.Boolean()
    }
)


@ns.route('/user/<int:user_id>')
class User(Resource):
    @jwt_required
    @admin_required
    @ns.marshal_with(_user_create_res)
    def get(self, user_id):
        user = services.admin.get_one_user(user_id)
        return user

    @jwt_required
    @admin_required
    @ns.marshal_with(_update_user_res)
    def put(self, user_id):
        user = services.admin.edit_user(user_id, request.form)
        return user

    @jwt_required
    @admin_required
    @ns.doc('delete user with id')
    def delete(self, user_id):
        message = services.admin.delete_user(user_id)
        return message
