from flask_restplus import Resource, fields
from flask_jwt_extended import jwt_required
from flask import request
from . import ns

from ducttapp import models, services
from ducttapp.helpers.decorators import admin_required


user_fields = ns.model('UserModel', models.UserSchema.schema_user_create_res)

user_list_fields = ns.model('ListUserModel', {
    'total': fields.Integer,
    'results': fields.List(fields.Nested(user_fields))
})


@ns.route('/users/')
class UserList(Resource):
    @ns.marshal_with(user_list_fields)
    @ns.doc(
        params={
            '_page': 'page number',
            '_limit': 'size in page',
            'q': 'key search',
            '_sort': 'Sort field',
            '_order': 'Sort type',
            'is_active': 'Filter status'
        }
    )
    @jwt_required
    @admin_required
    def get(self):
        params = request.args
        _page = params.get('_page') or 1
        _limit = params.get('_limit') or 10
        q = params.get('q') or ''
        _sort = params.get('_sort') or 'username'
        _order = params.get('_order') or 'descend'
        is_active = params.getlist('is_active[]')
        result = services.admin.get_all_users(_page, _limit, q, _sort, _order, is_active)
        return result
