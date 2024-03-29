from flask_restplus import Resource, fields
from flask_jwt_extended import jwt_required
from flask import request
from . import ns

from ducttapp import models, services

role_model = ns.model(
    name='Role',
    model=models.RoleSchema.role_res_schema
)


@ns.route('/roles/')
class RoleList(Resource):
    @ns.marshal_with(role_model)
    @jwt_required
    def get(self):
        roles = services.admin.get_all_roles()
        return roles
