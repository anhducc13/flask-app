from flask_restplus import Resource
from flask_jwt_extended import jwt_required, get_raw_jwt
from flask import make_response, after_this_request
from ducttapp import repositories
from . import ns


@ns.route('/logout')
class Logout(Resource):
    @jwt_required
    def get(self):
        jti = get_raw_jwt()['jti']
        repositories.revoked_token.save_revoked_token_to_database(jti=jti)
        logout_res = {
            'logout': True
        }
        @after_this_request
        def set_access_token_cookie(response):
            response.set_cookie('access_token_cookie', '', expires=0)
            return response
        return logout_res
