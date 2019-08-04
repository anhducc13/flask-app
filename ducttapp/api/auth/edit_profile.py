from flask_restplus import Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from ducttapp import models, services
from . import ns


role_model = ns.model(
    name='Role',
    model=models.RoleSchema.role_res_schema
)

user_fields = models.UserSchema.schema_user_create_res.copy()
user_fields.update({
    'roles': fields.List(fields.Nested(role_model))
})

edit_profile_model = ns.model(
    name='edit_profile_response',
    model=user_fields
)


@ns.route('/editProfile')
class EditProfile(Resource):
    @jwt_required
    @ns.marshal_with(edit_profile_model)
    def post(self):
        username = get_jwt_identity()
        user = services.auth.edit_profile_user(
            username=username,
            form_data=request.form
        )
        return user
