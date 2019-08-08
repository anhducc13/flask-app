from flask_restplus import Resource, fields
from ducttapp import helpers, repositories
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import ns

from ducttapp import models, services
from ducttapp.helpers.decorators import book_management_required

book_create_req = ns.model(
    name='book_create_req',
    model={
        'name': fields.String(required=True),
        'description': fields.String(required=True),
        'author': fields.String(),
        'is_active': fields.Boolean(),
        'price': fields.Float(required=True),
        'quantity_in_stock': fields.Integer(required=True),
        'categories': fields.List(fields.Integer())
    }
)

book_create_res = ns.model(
    name='book_create_res',
    model={
        'create': fields.Boolean()
    }
)


@ns.route('/')
class BookAdd(Resource):
    @ns.expect(book_create_req, validate=True)
    @ns.marshal_with(book_create_res)
    @jwt_required
    @book_management_required
    def post(self):
        data = request.json
        user_id = get_jwt_identity()
        services.book.add_book(user_id=user_id, **data)
        return {
            'create': True
        }
