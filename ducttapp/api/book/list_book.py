from flask_restplus import Resource, fields
from flask_jwt_extended import jwt_required
from flask import request
from . import ns

from ducttapp import models, services
from ducttapp.helpers.decorators import book_management_required

book_model = ns.model(
    name='BookModel',
    model={
        'id': fields.Integer(),
        'name': fields.String(),
        'description': fields.String(),
        'is_active': fields.Boolean(),
        'created_at': fields.DateTime(),
        'updated_at': fields.DateTime(),
        'user_created': fields.String(),
        'categories': fields.List(fields.Integer()),
        'quantity_in_stock': fields.Integer(),
        'price': fields.Float()
    })


book_list_model = ns.model(
    name='BookListModel',
    model={
        'total': fields.Integer(),
        'results': fields.List(fields.Nested(book_model))
    })


@ns.route('/list/')
class BookList(Resource):
    @ns.marshal_with(book_list_model)
    @ns.doc(
        params={
            '_page': 'page number',
            '_limit': 'size in page',
            'q': 'key search by name',
            '_sort': 'Sort field',
            '_order': 'Sort type',
            'is_active': 'Filter status'
        }
    )
    @jwt_required
    @book_management_required
    def get(self):
        params = request.args
        _page = params.get('_page') or 1
        _limit = params.get('_limit') or 10
        q = params.get('q') or ''
        _sort = params.get('_sort') or 'name'
        _order = params.get('_order') or 'descend'
        is_active = params.getlist('is_active[]')
        result = services.book.get_list_book(_page, _limit, q, _sort, _order, is_active)
        return result
