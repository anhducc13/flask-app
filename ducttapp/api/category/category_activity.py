from flask_restplus import Resource, fields
from flask import request
from flask_jwt_extended import jwt_required
from . import ns
import config

from ducttapp import models, services
from ducttapp.helpers.decorators import category_management_required

action_field = ns.model(
    name='ActionModel',
    model={
        'id': fields.Integer(),
        'log_name': fields.String(),
        'created_at': fields.DateTime(),
        'username': fields.String()
    }
)

category_action_list_field = ns.model('ListCategoryAction', {
    'total': fields.Integer,
    'results': fields.List(fields.Nested(action_field))
})


@ns.route('/activity')
class CategoryAction(Resource):
    @ns.marshal_with(category_action_list_field)
    @ns.doc(
        params={
            'category_id': 'Id',
            '_page': 'page number',
            '_limit': 'size in page',
            '_order': 'Sort type by created at',
        }
    )
    @jwt_required
    @category_management_required
    def get(self):
        params = request.args
        category_id = params.get('category_id') or None
        _page = params.get('_page') or 1
        _limit = params.get('_limit') or 10
        _order = params.get('_order') or 'descend'
        result = services.category.get_all_action(category_id, _page, _limit, _order)
        return result
