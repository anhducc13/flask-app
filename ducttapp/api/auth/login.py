from flask_restplus import Resource, fields
from flask import request, after_this_request
from flask_jwt_extended import create_access_token
from datetime import timedelta
from ducttapp import models, services, helpers
from . import ns

_login_req = ns.model(
    name='login_request',
    model={
        'username': fields.String(required=True, min_length=1),
        'password': fields.String(required=True, min_length=1)
    })

login_model = ns.model(
    name='login_model',
    model={
        'id': fields.Integer(),
        'email': fields.String(),
        'username': fields.String(),
        'is_admin': fields.Boolean(),
        'is_active': fields.Boolean(),
        'updated_at': fields.DateTime(),
        'fullname': fields.String(),
        'phone_number': fields.String(),
        'gender': fields.Boolean(),
        'birthday': fields.DateTime(),
        'avatar': fields.String(),
        'roles': fields.List(fields.Integer())
    }
)


@ns.route('/login')
class Login(Resource):
    @ns.expect(_login_req, validate=True)
    @ns.marshal_with(login_model)
    def post(self):
        data = request.json or request.args
        user = services.auth.lgin(**data)
        access_token = create_access_token(
            identity=user.id,
            expires_delta=timedelta(minutes=10)
        )

        @after_this_request
        def set_access_token_cookie(response):
            response.set_cookie(
                "access_token_cookie",
                access_token,
                max_age=timedelta(minutes=10),
            )
            return response

        return user.to_dict()


login_social_req = ns.model(
    name='login_social_request',
    model={
        'accessToken': fields.String(required=True, min_length=1),
    })


@ns.route('/loginGoogle/')
class LoginGoogle(Resource):
    @ns.expect(login_social_req, required=True)
    @ns.marshal_with(login_model)
    def post(self):
        token_google = request.json["tokenId"]
        info = helpers.google_token.get_info_from_token_google(token_google)
        gg_id = info['sub']
        username = f"user{info['sub']}"
        email = info['email']
        social_name = models.SocialName.GOOGLE
        user = services.auth.login_social(
            social_id=gg_id,
            username=username,
            email=email,
            social_name=social_name
        )
        access_token = create_access_token(
            identity=user.id,
            expires_delta=timedelta(minutes=10)
        )
        @after_this_request
        def set_access_token_cookie(response):
            response.set_cookie(
                "access_token_cookie",
                access_token,
                max_age=timedelta(minutes=10),
            )
            return response
        return user.to_dict()
