from flask_restplus import Resource
from flask_jwt_extended import jwt_required
from . import ns

from ducttapp import models, services
from ducttapp.helpers.decorators import admin_required

_user_create_res = ns.model('user_req', models.UserSchema.schema_user_create_res)


@jwt_required
@admin_required
@ns.route('/user/<int:user_id>')
class User(Resource):
    @ns.marshal_with(_user_create_res)
    def get(self, user_id):
        user = services.admin.get_one_user(user_id)
        return user

    @ns.doc('delete user with id')
    def delete(self, user_id):
        message = services.admin.delete_user(user_id)
        return message
