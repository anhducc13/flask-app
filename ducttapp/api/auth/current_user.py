from flask_restplus import Resource
from flask_jwt_extended import decode_token
from ducttapp import repositories, models
from flask import request
from . import ns

_current_user_res = ns.model(
    'current_user_res', models.UserSchema.schema_user_create_res)


@ns.route('/currentUser')
class CurrentUser(Resource):
    @ns.marshal_with(_current_user_res)
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
