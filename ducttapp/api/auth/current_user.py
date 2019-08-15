from flask_restplus import Resource, fields
from flask_jwt_extended import decode_token
from ducttapp import repositories, models
from flask import request
from . import ns

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


@ns.route('/currentUser')
class CurrentUser(Resource):
    @ns.marshal_with(user_model)
    def get(self):
        if 'access_token_cookie' not in request.cookies:
            return None
        try:
            raw_token = decode_token(request.cookies['access_token_cookie'])
            user_id = raw_token['identity']
            user = repositories.user.find_one_by_id(
                user_id=user_id
            )
            return user.to_dict() or None
        except ValueError:
            return None
