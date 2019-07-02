# from flask import Flask, request, jsonify
# from flask_restplus import Resource, Api, fields
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime, timedelta
# from sqlalchemy.orm import relationship
# from sqlalchemy import or_
# import flask_bcrypt as fb
# import re
# import jwt
# from ducttapp.extensions.exceptions import BadRequestException

# app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/user_management'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = 'ductt'

# api = Api(app)

# db = SQLAlchemy(app)
# bcrypt = fb.Bcrypt()


# class UserSchema:
#     signup_request_req = {
#         'email': fields.String(required=True, description='user email address'),
#         'username': fields.String(required=True, description='user username'),
#         'password': fields.String(required=True, description='user password')
#     }
#     signup_request_res = {
#         'email': fields.String(required=True, description='user email address'),
#         'username': fields.String(required=True, description='user username'),
#     }


# _signup_request_req = api.model(
#     'signup_request_req', UserSchema.signup_request_req)
# _signup_request_res = api.model(
#     'signup_request_res', UserSchema.signup_request_res)


# class Signup_Request(db.Model):
#     def __init__(self, **kwargs):
#         for k, v in kwargs.items():
#             setattr(self, k, v)
#         self.expired_time = (datetime.now() + timedelta(minutes=30))
#         self.create_token()

#     __tablename__ = 'signup_request'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     username = db.Column(db.String(128), nullable=False, unique=True)
#     email = db.Column(db.String(128), nullable=False, unique=True)
#     password_hash = db.Column(db.Text(), nullable=False)
#     is_admin = db.Column(db.Boolean, default=False)
#     expired_time = db.Column(db.TIMESTAMP, default=(datetime.now() + timedelta(minutes=30)))
#     user_token_confirm = db.Column(db.Text(), nullable=False)

#     @property
#     def password(self):
#         raise AttributeError('password: write-only field')

#     @password.setter
#     def password(self, password):
#         self.password_hash = bcrypt.generate_password_hash(
#             password).decode('utf-8')

#     def create_token(self):
#         token_data = {
#             "username" : self.username,
#             "exp": self.expired_time
#         }
#         token = jwt.encode(token_data, app.config['SECRET_KEY'], 'HS256')
#         self.user_token_confirm = token.decode('UTF-8')


# def save_user_to_signup_request(**kwargs):
#     user = Signup_Request(**kwargs)
#     db.session.add(user)
#     db.session.commit()
#     return user


# def find_one_by_email_or_username(email, username):
#     print(email)
#     print(username)
#     user1 = Signup_Request.query.filter(
#         or_(
#             Signup_Request.username == username,
#             Signup_Request.email == email
#         )
#     ).first()  # type: m.User

#     # user2 = Signup_Request.query.filter(
#     #     or_(
#     #         User.username == username,
#     #         User.email == email
#     #     )
#     # ).first()  # type: m.Signup_Request

#     return user1 or None


# @api.route('/register')
# class Register(Resource):
#     @api.expect(_signup_request_req, validate=True)
#     @api.marshal_with(_signup_request_res)
#     def post(self):
#         data = request.json or request.args

#         username = data['username']
#         email = data['email']
#         password = data['password']

#         if (
#             username and len(username) < 50 and
#             email and re.match(r"[^@]+@[^\.]+\..+", email) and
#             password and re.match(r"^[A-Za-z0-9]{6,}$", password)
#         ):
#             existed_user = find_one_by_email_or_username(email, username)
#             if existed_user:
#                 raise BadRequestException(
#                     "User with username {username} "
#                     "or email {email} already existed!".format(
#                         username=username,
#                         email=email
#                     )
#                 )

#             user = save_user_to_signup_request(
#                 username=username,
#                 email=email,
#                 password=password
#             )
#             return user
#         else:
#             raise BadRequestException("Invalid user data specified!")


# if __name__ == '__main__':
#     app.run(debug=True)
