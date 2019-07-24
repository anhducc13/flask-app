from flask_restplus import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from ducttapp import repositories
from . import ns
from flask import request


@ns.route('/currentUser')
class CurrentUser(Resource):
  @jwt_required
  def get(self):
    username = get_jwt_identity()
    user = repositories.user.find_one_by_email_or_username_in_user_ignore_case(username=username)
    return user.to_dict(), 200
