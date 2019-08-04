from flask_restplus import Resource, fields
from flask_jwt_extended import decode_token
from ducttapp import repositories, models
from flask import request
from . import ns


role_model = ns.model(
    name='Role',
    model=models.RoleSchema.role_res_schema
)

user_fields = models.UserSchema.schema_user_create_res.copy()
user_fields.update({
    'roles': fields.List(fields.Nested(role_model))
})

user_model = ns.model(
    'current_user_res', user_fields)


@ns.route('/currentUser')
class CurrentUser(Resource):
    @ns.marshal_with(user_model)
    def get(self):
        if 'access_token_cookie' not in request.cookies:
            return None
        try:
            raw_token = decode_token(request.cookies['access_token_cookie'])
            username = raw_token['identity']
            user = repositories.user.find_one_by_email_or_username_in_user_ignore_case(
                username=username
            )
            return user
        except:
            return None
