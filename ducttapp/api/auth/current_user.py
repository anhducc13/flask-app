from flask_restplus import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from ducttapp import repositories, models
from . import ns

_current_user_res = ns.model(
  'current_user_res', models.UserSchema.schema_user_create_res)


@ns.route('/currentUser')
class CurrentUser(Resource):
  @ns.marshal_with(_current_user_res)
  @jwt_required
  def get(self):
    username = get_jwt_identity()
    user = repositories.user.find_one_by_email_or_username_in_user_ignore_case(username=username)
    return user
