from flask_restplus import Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from . import ns

from ducttapp import models, services
from ducttapp.helpers.decorators import category_management_required

category_model = ns.model(
    name='CategoryModel',
    model={
        'id': fields.Integer(),
        'name': fields.String(),
        'description': fields.String(),
        'is_active': fields.Boolean(),
        'created_at': fields.DateTime(),
        'updated_at': fields.DateTime(),
        'user_created': fields.String()
    })

update_category_res = ns.model(
    name="update_category_response",
    model={
        "update": fields.Boolean()
    }
)


@ns.route('/<int:category_id>')
class Category(Resource):
    @jwt_required
    @category_management_required
    @ns.marshal_with(category_model)
    def get(self, category_id):
        category = services.category.get_one_category(category_id)
        return category.to_dict()

    @jwt_required
    @category_management_required
    @ns.marshal_with(update_category_res)
    def put(self, category_id):
        user_id = get_jwt_identity()
        data = request.json
        result = services.category.edit_category(user_id, category_id, **data)
        return result

    @jwt_required
    @category_management_required
    @ns.doc('delete category by id')
    def delete(self, category_id):
        message = services.category.delete_category(category_id)
        return message

