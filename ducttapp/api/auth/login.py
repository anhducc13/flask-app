from flask_restplus import Resource
from flask import request, make_response
from flask_jwt_extended import create_access_token
from datetime import timedelta
from ducttapp import models, services
from . import ns

_login_req = ns.model(
    'login_request', models.UserSchema.schema_login_req)


@ns.route('/login')
class Login(Resource):
    @ns.expect(_login_req, validate=True)
    def post(self):
        print(request.headers)
        data = request.json or request.args
        user = services.auth.login(**data)
        access_token = create_access_token(identity=user.username, expires_delta=timedelta(minutes=10))
        login_res = {
            "login": True,
            "username": user.username
        }
        resp = make_response(login_res)
        resp.set_cookie("access_token_cookie", access_token, max_age=timedelta(minutes=10), httponly=True)
        return resp
