from flask_restplus import Resource, fields
from ducttapp import helpers, repositories
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import ns

from ducttapp import models, services
from ducttapp.helpers.decorators import category_management_required

category_create_req = ns.model(
    name='category_create_req',
    model={
        'name': fields.String(required=True),
        'description': fields.String(required=True),
    }
)

category_create_res = ns.model(
    name='category_create_res',
    model={
        'create': fields.Boolean()
    }
)


@ns.route('/')
class CategoryAdd(Resource):
    @ns.expect(category_create_req, validate=True)
    @jwt_required
    @category_management_required
    def post(self):
        data = request.json
        username = get_jwt_identity()
        services.category.add_category(username=username, **data)
        return {
            'create': True
        }