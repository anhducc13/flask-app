from ducttapp.models import db, bcrypt
from datetime import datetime, timedelta
from flask_restplus import fields
from ducttapp import helpers


class Signup_Request(db.Model):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.expired_time = (datetime.now() + timedelta(minutes=30))

    __tablename__ = 'signup_request'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(
        db.String(128, collation='utf8mb4_general_ci', convert_unicode=True), nullable=False, unique=True)
    email = db.Column(db.String(128, collation='utf8mb4_general_ci', convert_unicode=True), nullable=False, unique=True)
    password_hash = db.Column(db.Text(collation='utf8mb4_general_ci', convert_unicode=True), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    expired_time = db.Column(db.TIMESTAMP, default=(datetime.now() + timedelta(minutes=30)))
    user_token_confirm = db.Column(db.Text(collation='utf8mb4_general_ci', convert_unicode=True), nullable=False)

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
            "email": self.email,
            "user_token_confirm": self.user_token_confirm
        }


class SignupSchema:
    signup_request_req = {
        'email': fields.String(
            required=True,
            description='user email',
            pattern=helpers.validators.REGEX_EMAIL
        ),
        'username': fields.String(
            required=True,
            description='user username',
            pattern=helpers.validators.REGEX_USERNAME
        ),
        'password': fields.String(
            required=True,
            description='user password',
            pattern=helpers.validators.REGEX_PASSWORD
        )
    }
    signup_request_res = {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
    }
