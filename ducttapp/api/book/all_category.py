from flask_restplus import Resource, fields
from flask_jwt_extended import jwt_required
from flask import request
from . import ns

from ducttapp import models, services
from ducttapp.helpers.decorators import book_management_required

category_model = ns.model(
    name='Category',
    model={
        'id': fields.Integer(),
        'name': fields.String(),
    }
)


@ns.route('/allCategory')
class AllCategory(Resource):
    @ns.marshal_list_with(category_model)
    @jwt_required
    @book_management_required
    def get(self):
        categories = models.Category.query.all()
        return categories
