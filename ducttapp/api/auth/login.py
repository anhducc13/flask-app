from flask_restplus import Resource, fields
from flask import request, after_this_request
from flask_jwt_extended import create_access_token
from datetime import timedelta
from ducttapp import models, services
from . import ns

_login_req = ns.model(
    'login_request', models.UserSchema.schema_login_req)

_login_social_req = ns.model(
    name='login_social_request',
    model={
        'email': fields.String(required=True)
    }
)

_login_res = ns.model(
    'login_response', models.UserSchema.schema_user_create_res)


@ns.route('/login')
class Login(Resource):
    @ns.expect(_login_req, validate=True)
    @ns.marshal_with(_login_res)
    def post(self):
        data = request.json or request.args
        user = services.auth.login(**data)
        access_token = create_access_token(
            identity=user.username,
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
        return user


@ns.route('/loginSocial')
class LoginSocial(Resource):
    @ns.expect(_login_social_req, validate=True)
    @ns.marshal_with(_login_res)
    def post(self):
        pass
