from flask_restplus import Namespace, Resource
from flask import request

from ducttapp import models, services

ns = Namespace('admin', description='User operators')
parser = ns.parser()
parser.add_argument('user_id', location='args', help='User Id request')

_user_res = ns.model('user_res', models.UserSchema.user)
_user_req = ns.model('user_req', models.UserSchema.user_create_req)


@ns.route('/users')
class UserList(Resource):
  @ns.marshal_list_with(_user_res)
  def get(self):
    users = services.admin.get_all_users()
    return users


@ns.route('/user')
class UserAdd(Resource):
  @ns.expect(_user_req, validate=True)
  @ns.marshal_with(_user_res)
  def post(self):
    data = request.json or request.params
    user = services.admin.add_user(**data)
    return user


@ns.route('/user/<int:user_id>')
class User(Resource):
  @ns.marshal_with(_user_res)
  def get(self, user_id):
    user = services.admin.get_one_user(user_id)
    return user

  @ns.doc('delete user with id')
  def delete(self, user_id):
    message = services.admin.delete_user(user_id)
    return message

