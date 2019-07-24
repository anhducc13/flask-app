from flask_restplus import Resource, reqparse
from flask_jwt_extended import jwt_required
from . import ns

from ducttapp import models, services
from ducttapp.helpers.decorators import admin_required

_user_create_res = ns.model('user_req', models.UserSchema.schema_user_create_res)


@ns.route('/users')
class UserList(Resource):
    @ns.marshal_list_with(_user_create_res)
    @ns.doc(
        params={
            '_page': 'page number',
            '_limit': 'size in page',
            'q': 'key search',
            '_sort': 'Sort field',
            '_order': 'Sort type'
        }
    )
    @jwt_required
    @admin_required
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
        _order = args.get('_order') or 'desc'
        users = services.admin.get_all_users(_page, _limit, q, _sort, _order)
        return users
