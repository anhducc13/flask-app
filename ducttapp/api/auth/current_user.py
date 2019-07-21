from flask_restplus import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from . import ns


@ns.route('/currentUser')
class CurrentUser(Resource):
  @jwt_required
  def get(self):
    username = get_jwt_identity()
    return {
             'username': username
           }, 200
