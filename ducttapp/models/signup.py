from ducttapp.models import db, bcrypt
import config
from datetime import datetime, timedelta
from flask_restplus import fields
from ducttapp.helpers import token


class Signup_Request(db.Model):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.expired_time = (datetime.now() + timedelta(minutes=30))
        self.create_token()

    __tablename__ = 'signup_request'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False, unique=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password_hash = db.Column(db.Text(), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    expired_time = db.Column(db.TIMESTAMP, default=(datetime.now() + timedelta(minutes=30)))
    user_token_confirm = db.Column(db.Text(), nullable=False)

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(
            password).decode('utf-8')

    def create_token(self):
        token_data = {
            "username" : self.username,
        }
        token_string = token.encode_token(token_data)
        self.user_token_confirm = token_string.decode('UTF-8')

class SignupSchema:
    signup_request_req = {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password')
    }
    signup_request_res = {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
    }