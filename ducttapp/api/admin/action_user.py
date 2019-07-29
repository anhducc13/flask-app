from flask_restplus import Resource, fields
from flask import request
from flask_jwt_extended import jwt_required
from . import ns
import config

from ducttapp import models, services
from ducttapp.helpers.decorators import admin_required

action_field = ns.model(
    'ActionModel', models.user_action.schema_user_action_res)

user_action_list_field = ns.model('ListUserAction', {
    'total': fields.Integer,
    'results': fields.List(fields.Nested(action_field))
})


@ns.route('/user/action')
class UserAction(Resource):
    @ns.marshal_with(user_action_list_field)
    @ns.doc(
        params={
            'user_id': 'Id',
            '_page': 'page number',
            '_limit': 'size in page',
            '_order': 'Sort type by created at',
            'action_name': 'Filter action name'
        }
    )
    @jwt_required
    @admin_required
    def get(self):
        params = request.args
        user_id = params.get('user_id') or 1
        _page = params.get('_page') or 1
        _limit = params.get('_limit') or 10
        _order = params.get('_order') or 'descend'
        action_name = params.getlist('action_name[]') \
            or [config.CREATED, config.LOGIN, config.LOGOUT, config.LOCK,
                config.FORGOT_PASSWORD, config.UPDATE_PASSWORD]
        result = services.admin.get_all_action(int(user_id), int(_page), int(_limit), _order, action_name)
        return result
