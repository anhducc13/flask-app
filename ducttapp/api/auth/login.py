from flask_restplus import Resource, fields
from flask import request, after_this_request
from flask_jwt_extended import create_access_token
from datetime import timedelta
from ducttapp import models, services
from . import ns

_login_req = ns.model(
    name='login_request',
    model={
        'username': fields.String(required=True, min_length=1),
        'password': fields.String(required=True, min_length=1)
    })

role_model = ns.model(
    name='Role',
    model=models.RoleSchema.role_res_schema
)

login_fields = models.UserSchema.schema_user_create_res.copy()
login_fields.update({
    'roles': fields.List(fields.Nested(role_model))
})

login_model = ns.model(
    name='login_response',
    model=login_fields
)


@ns.route('/login')
class Login(Resource):
    @ns.expect(_login_req, validate=True)
    @ns.marshal_with(login_model)
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
