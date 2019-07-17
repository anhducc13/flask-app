from flask_restplus import Resource
from flask_jwt_extended import jwt_required, get_raw_jwt
from ducttapp import services
from . import ns


@ns.route('/logout')
class Logout(Resource):
    @jwt_required
    def get(self):
        jti = get_raw_jwt()['jti']
        return services.auth.logout(jti)
