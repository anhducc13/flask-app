from flask_restplus import Resource
from flask import request
from flask_jwt_extended import jwt_required
from . import ns

from ducttapp import models, services
from ducttapp.helpers.decorators import admin_required

_user_create_req = ns.model('user_res', models.UserSchema.schema_user_create_req)
_user_create_res = ns.model('user_req', models.UserSchema.schema_user_create_res)


@ns.route('/user')
class UserAdd(Resource):
    @ns.expect(_user_create_req, validate=True)
    @ns.marshal_with(_user_create_res)
    @jwt_required
    @admin_required
    def post(self):
        data = request.json
        user = services.admin.add_user(**data)
        return user
