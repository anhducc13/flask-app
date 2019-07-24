from ducttapp.models import db, bcrypt
from datetime import datetime
from flask_restplus import fields
from sqlalchemy.orm import relationship
from ducttapp import helpers


class User(db.Model):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False, unique=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    created_at = db.Column(db.TIMESTAMP, default=datetime.now)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.now)
    password_hash = db.Column(db.Text(), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.TIMESTAMP, nullable=True)
    history_pass_change = relationship("HistoryPassChange")

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(
            password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def update_attr(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.updated_at = datetime.now()

    def update_last_login(self):
        self.last_login = datetime.now()

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_admin': self.is_admin,
            'is_active': self.is_active,
            'last_login': self.last_login,
        }


class UserSchema:
    schema_user_create_req = {
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
        'is_admin': fields.Boolean(required=True, description='Admin or not'),
    }

    schema_user_create_res = {
        'id': fields.Integer(required=True, description='user id'),
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'is_admin': fields.Boolean(required=True, description='Admin or not'),
    }

    schema_login_req = {
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
    schema_login_res = {
        'login': fields.Boolean(required=True, description='Login'),
        'username': fields.String(required=True, description='user name login'),
        # 'accessToken': fields.String(required=True, description='access token login'),
        # 'timeExpired': fields.Float(required=True, description='time expired login session'),
        # 'isAdmin': fields.Boolean(required=True, description='Admin or not')
    }
    schema_update_password_req = {
        'old_password': fields.String(
            required=True,
            description='user old password',
            pattern=helpers.validators.REGEX_PASSWORD
        ),
        'new_password': fields.String(
            required=True,
            description='user new password',
            pattern=helpers.validators.REGEX_PASSWORD
        ),
    }
    schema_forgot_password_req = {
        'username': fields.String(
            required=True,
            description='user username',
            pattern=helpers.validators.REGEX_USERNAME
        ),
        'email': fields.String(
            required=True,
            description='user email',
            pattern=helpers.validators.REGEX_EMAIL
        ),
    }
    schema_notify_res = {
        'ok': fields.Boolean(required=True, description='Task success or not'),
    }





