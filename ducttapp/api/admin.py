from flask_restplus import Namespace, Resource, reqparse
from flask import request

from ducttapp import models, services

ns = Namespace('admin', description='User operators')

_user_res = ns.model('user_res', models.UserSchema.user)
_user_req = ns.model('user_req', models.UserSchema.user_create_req)


@ns.route('/users')
class UserList(Resource):
    @ns.marshal_list_with(_user_res)
    @ns.doc(
        params={
            '_page': 'page number',
            '_limit': 'size in page',
            'q': 'key search',
            '_sort': 'Sort field',
            '_order': 'Sort type'
        }
    )
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('_page', required=False,
                            location='args', help='page number')
        parser.add_argument('_limit', required=False,
                            location='args', help='size in page')
        parser.add_argument('q', required=False,
                            location='args', help='key search')
        parser.add_argument('_sort', required=False,
                            location='args', help='Sort field')
        parser.add_argument('_order', required=False,
                            location='args', help='Sort type')
        args = parser.parse_args()
        _page = args.get('_page') or 1
        _limit = args.get('_limit') or 10
        q = args.get('q') or ''
        _sort = args.get('_sort') or 'username'
        _order = 'DESC' if args.get('_order') == 'DESC' else 'ASC'
        users = services.admin.get_all_users(_page, _limit, q, _sort, _order)
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
