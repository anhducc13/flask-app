from flask_restplus import Namespace, Resource, fields
from flask import request

from ducttapp import models, services, extensions

ns = Namespace('admin', description='User operators')

@ns.route('/users')
class UserList(Resource):
  def get(self):
    return {"message": "ductt"}, 201

@ns.route('/user/<int:id>')
class User(Resource):
  def get(self):
    return {"message": "ducttssffds"}, 201