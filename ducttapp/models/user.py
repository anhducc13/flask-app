from ducttapp.models import db, bcrypt
from datetime import datetime
from flask_restplus import fields
from sqlalchemy.orm import relationship
from ducttapp import helpers
from .base import TimestampMixin
from .role import user_role_table


class User(db.Model, TimestampMixin):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False, unique=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    fullname = db.Column(db.String(128), nullable=True)
    gender = db.Column(db.Boolean, nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)
    birthday = db.Column(db.DateTime, nullable=True)
    avatar = db.Column(db.String(256), nullable=True)
    password_hash = db.Column(db.Text(), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    time_unlock = db.Column(db.TIMESTAMP, default=datetime.now)
    history_pass_change = relationship("HistoryPassChange", cascade="save-update, merge, delete")
    history_wrong_pass = relationship("HistoryWrongPass", cascade="save-update, merge, delete")
    user_action = relationship("UserAction", cascade="save-update, merge, delete")
    roles = relationship(
        "Role",
        secondary=user_role_table,
        back_populates="users")
    categories = relationship("UserCategoryAction", back_populates="user")

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

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_admin': self.is_admin,
            'is_active': self.is_active,
            'updated_at': datetime.timestamp(self.updated_at),
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
        'is_admin': fields.Boolean(required=True, description='Admin or none'),
        'is_active': fields.Boolean(required=True, description='Active or inactive'),
        'updated_at': fields.DateTime(required=True, description='Updated at'),
        'fullname': fields.String(),
        'phone_number': fields.String(),
        'gender': fields.Boolean(),
        'birthday': fields.DateTime(),
        'avatar': fields.String(),
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





