from ducttapp.models import db, bcrypt
from datetime import datetime, timedelta
from flask_restplus import fields
from ducttapp import helpers
import enum


class SocialName(enum.Enum):
    FACEBOOK = 'FACEBOOK'
    GOOGLE = 'GOOGLE'


class SocialLogin(db.Model):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    __tablename__ = 'social_login'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    social_id = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    created_at = db.Column(db.TIMESTAMP, default=datetime.now)
    social_name = db.Column(db.Enum(SocialName), nullable=False)
