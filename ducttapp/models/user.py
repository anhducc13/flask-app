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
    username = db.Column(
        db.String(128, convert_unicode=True), nullable=False)
    email = db.Column(db.String(128, convert_unicode=True), nullable=False, unique=True)
    fullname = db.Column(db.String(128, convert_unicode=True), nullable=True)
    gender = db.Column(db.Boolean, nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)
    birthday = db.Column(db.DateTime, nullable=True)
    avatar = db.Column(db.String(256), nullable=True)
    password_hash = db.Column(db.Text(convert_unicode=True), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    time_unlock = db.Column(db.TIMESTAMP, default=datetime.now)
    history_pass_change = relationship("HistoryPassChange", cascade="save-update, merge, delete")
    history_wrong_pass = relationship("HistoryWrongPass", cascade="save-update, merge, delete")
    user_action = relationship("UserAction", cascade="save-update, merge, delete")
    social_login = relationship("SocialLogin", cascade="save-update, merge, delete")
    roles = relationship(
        "Role",
        secondary=user_role_table,
        back_populates="users")
    categories = relationship("UserCategoryAction", back_populates="user", cascade="all, delete-orphan")
    books = relationship("UserBookAction", back_populates="user", cascade="all, delete-orphan")

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
            'email': self.email,
            'username': self.username,
            'is_active': self.is_active,
            'updated_at': self.updated_at,
            'fullname': self.fullname,
            'phone_number': self.phone_number,
            'gender': self.gender,
            'birthday': self.birthday,
            'avatar': self.avatar,
            'roles': [r.id for r in self.roles]
        }