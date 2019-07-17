from flask_restplus import Resource
from ducttapp import services
from . import ns


@ns.route('/verify/<string:token>', endpoint='verify')
class Verify(Resource):
    def get(self, token):
        message = services.auth.verify(token)
        return message
