from ducttapp.models import db, bcrypt
from datetime import datetime, timedelta
from flask_restplus import fields
import uuid


class Signup_Request(db.Model):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.expired_time = (datetime.now() + timedelta(minutes=30))

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

    def token_verify_expired(self):
        return self.expired_time < datetime.now()

    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email
        }


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
